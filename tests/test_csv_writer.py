import tempfile
import os
from rover.utils.csv_writer import CSVWriter


class DummySitter:
    def __init__(self, email, name, ratings_score, num_stays):
        self.email = email
        self.name = name
        self.ratings_score = ratings_score
        self.num_stays = num_stays


class DummyScoringService:
    def calculate_all_scores(self, sitter):
        return {
            "email": sitter.email,
            "name": sitter.name,
            "profile_score": "4.00",
            "ratings_score": "5.00",
            "search_score": "4.50",
        }


def test_write_sitters_scores():
    dummy_sitter = DummySitter("test@example.com", "John Doe", 5.0, 3)
    sitters_dict = {"test@example.com": dummy_sitter}
    scoring_service = DummyScoringService()

    with tempfile.TemporaryDirectory() as tmpdirname:
        output_file = os.path.join(tmpdirname, "sitters.csv")

        count = CSVWriter.write_sitters_scores(
            output_file, sitters_dict, scoring_service
        )

        assert count == 1
        assert os.path.exists(output_file)

        with open(output_file, "r") as f:
            lines = f.readlines()
            assert len(lines) == 2  # header + 1 row
            assert "email,name,profile_score,ratings_score,search_score" in lines[0]
            assert "test@example.com" in lines[1]
