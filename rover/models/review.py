class Review:
    """Represents a single review left by a customer after a stay."""

    def __init__(
        self, rating: float, start_date: str, end_date: str, dogs: str, text: str
    ):
        self.rating = rating  # Rating score (1-5)
        self.start_date = start_date  # Start date of stay (YYYY-MM-DD)
        self.end_date = end_date  # End date of stay (YYYY-MM-DD)
        self.dogs = dogs  # Dogs involved in the stay (string list)
        self.text = text  # Review text provided by the owner
