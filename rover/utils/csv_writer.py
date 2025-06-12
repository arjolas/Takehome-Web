import csv
import os
from rover.models.sitter_score_dto import SitterScoreDTO
from rover.services.scoring_service import ScoringService


class CSVWriter:
    @staticmethod
    def write_sitters_scores(
        output_path: str, sitters_dict: dict, scoring_service: ScoringService
    ) -> int:
        # Ensure output directory exists
        os.makedirs(os.path.dirname(output_path), exist_ok=True)

        with open(output_path, mode="w", newline="") as file:
            writer = csv.DictWriter(file, fieldnames=SitterScoreDTO.fields)
            writer.writeheader()

            count = 0
            for sitter in sitters_dict.values():
                scores = scoring_service.calculate_all_scores(sitter)
                writer.writerow(scores)
                count += 1

        return count
