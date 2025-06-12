import string
from rover.models.sitter import Sitter
from rover.utils.logger import get_logger

logger = get_logger(__name__)


class ScoringService:
    """Service class responsible for calculating profile, rating and search scores."""

    @staticmethod
    def calculate_profile_score(name: str) -> float:
        """Calculates profile score based on distinct alphabet coverage."""
        name = name.lower()
        letters = set(c for c in name if c in string.ascii_lowercase)
        score = round(5 * (len(letters) / 26), 2)

        logger.info("Calculated profile score: %.2f for name: %s", score, name)
        return score

    @staticmethod
    def calculate_search_score(
        profile_score: float, ratings_score: float, num_stays: int
    ) -> float:
        if num_stays == 0:
            score = profile_score
        elif num_stays >= 10:
            score = ratings_score
        else:
            score = profile_score + (ratings_score - profile_score) * (num_stays / 10)
            score = round(score, 2)

        logger.info("Calculated search score: %.2f", score)
        return score

    def calculate_all_scores(self, sitter: Sitter) -> dict:
        """Calculates and returns all scores for a sitter."""
        profile_score = self.calculate_profile_score(sitter.name)
        ratings_score = sitter.ratings_score
        search_score = self.calculate_search_score(
            profile_score, ratings_score, sitter.num_stays
        )

        return {
            "email": sitter.email,
            "name": sitter.name,
            "profile_score": f"{profile_score:.2f}",
            "ratings_score": f"{ratings_score:.2f}",
            "search_score": f"{search_score:.2f}",
        }
