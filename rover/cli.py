import argparse
from rover.repository.csv_repository import CSVRepository
from rover.services.scoring_service import ScoringService
from rover.utils.csv_writer import CSVWriter
from rover.utils.logger import get_logger

logger = get_logger(__name__)


def main():
    parser = argparse.ArgumentParser(description="Rover Scoring Calculator")
    parser.add_argument("--input", "-i", required=True, help="Path to input CSV file")
    parser.add_argument(
        "--output",
        "-o",
        default="output/sitters.csv",
        help="Path to output CSV file (default: output/sitters.csv)",
    )

    args = parser.parse_args()

    logger.info("Loading data from input CSV: %s", args.input)
    repo = CSVRepository(args.input)
    sitters_dict = repo.load_sitters()
    logger.info("Loaded %d sitters from input file.", len(sitters_dict))

    scoring_service = ScoringService()

    count = CSVWriter.write_sitters_scores(args.output, sitters_dict, scoring_service)

    logger.info("Successfully processed %d sitters.", count)
    logger.info("Output written to: %s", args.output)


if __name__ == "__main__":
    main()
