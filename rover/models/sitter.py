from typing import List
from rover.models.review import Review


class Sitter:
    """Represents a pet sitter with associated reviews."""

    def __init__(self, email: str, name: str):
        self.email = email  # Unique sitter email (acts as identifier)
        self.name = name  # Sitter's full name
        self.reviews: List[Review] = []  # Collection of Review objects

    def add_review(self, review: Review):
        """Adds a review to this sitter."""
        self.reviews.append(review)

    @property
    def num_stays(self) -> int:
        """Returns total number of stays (reviews)."""
        return len(self.reviews)

    @property
    def ratings_score(self) -> float:
        """Calculates the average rating score."""
        if not self.reviews:
            return 0.0
        return round(sum(r.rating for r in self.reviews) / len(self.reviews), 2)
