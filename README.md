
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
python -m rover.cli --input data/data.csv

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

Tool_________________|Purpose________________
black	                Auto-code formatter
flake8	              Linter for code style
mypy	                Static type checker
pytest	              Unit testing framework
pre-commit	          Automates quality checks on commit

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

---

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

1. **How would you adjust the calculation and storage of search scores in a production application?**

2. **Describe a technical implementation for the frontend you would use to display a list of sitters and their scores. How would the frontend manage state as users interact with a page?**

2. **What infrastructure choices might you make to build and host this project at scale? Suppose your web application must return fast search results with a peak of 10 searches per second.**

4. **Describe how you would approach API design for a backend service to provide sitter and rank data to a client/web frontend.**
