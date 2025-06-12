import csv
import os
from rover.models.sitter_score_dto import SitterScoreDTO
from rover.services.scoring_service import ScoringService


class CSVWriter:
    @staticmethod
    def write_sitters_scores(
        output_path: str, sitters_dict: dict, scoring_service: ScoringService
    ) -> int:
        os.makedirs(os.path.dirname(output_path), exist_ok=True)

        all_scores = []

        # Calculate all scores first
        for sitter in sitters_dict.values():
            scores = scoring_service.calculate_all_scores(sitter)
            all_scores.append(scores)

        # Sort descending by search_score
        all_scores_sorted = sorted(
            all_scores, key=lambda x: float(x["search_score"]), reverse=True
        )

        with open(output_path, mode="w", newline="") as file:
            writer = csv.DictWriter(file, fieldnames=SitterScoreDTO.fields)
            writer.writeheader()

            for scores in all_scores_sorted:
                writer.writerow(scores)

        return len(all_scores_sorted)
