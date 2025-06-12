import pandas as pd
from rover.models.sitter import Sitter
from rover.models.review import Review


class CSVRepository:
    """Repository class responsible for loading sitters and reviews from CSV."""

    def __init__(self, csv_path: str):
        self.csv_path = csv_path

    def load_sitters(self) -> dict:
        """Loads data and returns a dictionary of sitters indexed by email."""
        df = pd.read_csv(self.csv_path)
        sitters = {}

        for _, row in df.iterrows():
            email = row["sitter_email"]
            name = row["sitter"]
            rating = row["rating"]
            start_date = row["start_date"]
            end_date = row["end_date"]
            dogs = row["dogs"]
            text = row["text"]

            review = Review(rating, start_date, end_date, dogs, text)

            if email not in sitters:
                sitter = Sitter(email, name)
                sitters[email] = sitter
            else:
                sitter = sitters[email]

            sitter.add_review(review)

        return sitters
