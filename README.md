
# Rover Coding Project Solution

This project implements the Rover search ranking system as described in the coding assignment.  
The solution follows Object-Oriented Design (OOP), Domain Driven Design (DDD) principles, and applies SOLID best practices.

---

## Project Structure

- `rover/models/` - Domain models (`Sitter`, `Review`)
- `rover/repository/` - Data access layer (CSV Reader)
- `rover/services/` - Business logic (score calculations)
- `rover/cli.py` - Application entry point
- `tests/` - Unit tests

---

## Setup & Run

### Install dependencies

```bash
pip install -r requirements.txt
```

### Execute main program

```bash
# Default output
python -m rover.cli --input data/reviews.csv

# Custom output
python -m rover.cli --input input/data.csv --output output/my_custom_output.csv

```

### The output will be generated

```
output/sitters.csv
```

### Run tests

```bash
pytest --cov=rover/services --cov=rover/utils --cov-fail-under=80
```

### Automation & Code Quality
### This project includes full pre-commit automation and code quality tools:

| Tool         | Purpose                          | Config Location     | Enforced in Pre-Commit |
|--------------|-----------------------------------|----------------------|------------------------|
| `black`      | Code autoformatter (PEP8 + 88 cols) | `.pre-commit-config.yaml` |  
| `pytest`     | Unit tests runner                 | N/A                  |
| `pytest-cov` | Code coverage enforcement (80%)  | `.pre-commit-config.yaml`  |
| `pre-commit` | Hook runner for automation        | `.pre-commit-config.yaml` |

```bash
pre-commit run --all-files
```
---

## Domain Model Description

- **Sitter**:  
  Represents a pet sitter including their name, email, and associated reviews.

- **Review**:  
  Represents an individual stay, including:
  - `rating`: numeric review score
  - `start_date` and `end_date`: stay period
  - `dogs`: dogs involved in the stay
  - `text`: customer review comment


## Scoring Algorithm

- **Profile Score:**  
  `5 * (fraction of distinct letters in sitter's name / 26 letters of alphabet)`

- **Ratings Score:**  
  Average of all stay ratings.

- **Search Score:**  
  - If stays == 0: equal to profile score  
  - If stays >= 10: equal to ratings score  
  - If 1 <= stays < 10: interpolated weighted average between profile and ratings score

_All scores are rounded to 2 decimal places._

---

## Design Choices & Principles

- Applied **Domain Driven Design (DDD)**
- Applied **SOLID Principles**
- Applied **Separation of Concerns**
- Fully **extensible and maintainable architecture**


## Discussion Question

Imagine you are designing a Rover-like production web application based on this coding exercise. 
The application will compute search scores for sitters, return a list of search results based on those scores, 
and display them through a web UI.

Please answer ONE of the following questions on how you would approach the design:

**How would you adjust the calculation and storage of search scores in a production application?**

### System Requirements

- The Search Score combines both static data (sitter name) and dynamic data (reviews).
- Search operations require fast query performance and low latency.
- Updates to Search Score are triggered only when new reviews are submitted or existing reviews are modified.
- The system must remain scalable as the dataset grows (more sitters and reviews).

### Proposed Architecture

#### Decouple Review Ingestion and Score Calculation

- Each time a new review is submitted, it is written to a normalized `reviews` table in a relational database.
- After writing the review, the service publishes an event (`ReviewCreated`) into a message queue (Kafka, RabbitMQ, or AWS SNS/SQS).

#### Asynchronous Score Calculation

- A dedicated worker service listens to the event queue.
- When triggered, the worker retrieves all reviews for the corresponding sitter, recalculates:
  - Ratings Score
  - Search Score
- Profile Score is static and calculated once at sitter creation.

#### Precomputed Scores Storage

- The recalculated scores are written into a materialized `sitter_scores` table:

```sql
sitter_scores (
  sitter_id PK,
  profile_score FLOAT,
  ratings_score FLOAT,
  search_score FLOAT,
  last_updated TIMESTAMP
)
```

#### Search Service Read Path

- The search API queries directly the precomputed `sitter_scores` table.
- This allows very fast search query response times.

#### Caching Layer (Optional)

- Redis or Memcached can be added to cache frequent search queries or hot sitter profiles.

#### Monitoring & Logging
- Centralized logging using ELK stack (Elasticsearch, Logstash, Kibana) or modern SaaS (e.g. Datadog, New Relic, Splunk).

#### Architecture components
| Component       | Description |
|------------------|-------------|
| **Frontend Web Application** | Web UI for end-users to browse sitter search results |
| **API Gateway / Load Balancer** | Routes incoming HTTP requests to backend services |
| **Search API Service** | Stateless service serving search results, reading precomputed scores |
| **Relational Database** | Stores normalized `sitters` and `reviews` tables |
| **Precomputed Scores Table** | Materialized `sitter_scores` table for fast search reads |
| **Message Queue** | Decouples review ingestion and scoring updates |
| **Score Calculation Worker** | Listens to queue events and recalculates sitter scores asynchronously |
| **Redis Cache** | Caches hot sitter scores and frequent search queries |
| **Monitoring & Logging Stack** | Centralized observability using Prometheus, Grafana, ELK stack | 


### Data Flow Overview

**Review Submission**
- User submits a review via frontend.
- Review is written into `reviews` table.
- Review event (`ReviewCreated`) is published into message queue.

**Score Calculation**
- Worker service consumes `ReviewCreated` events.
- Worker fetches sitter's reviews, recalculates scores.
- Updated scores are written into `sitter_scores` table.

**Search Requests**

- User submits search query via web UI.
- Search API queries `sitter_scores` directly.
- Redis is used to cache frequent search results.
