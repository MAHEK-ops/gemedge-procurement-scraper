"""
Main entry point for GemEdge scraper

Modes:
--fetch : Fetch listing pages + result pages
--parse : Parse saved HTML + clean data + generate insights
"""

import argparse
import sys
import pandas as pd

from utils.logger import setup_logger
from utils.file_manager import FileManager
from utils.saver import DataSaver

from scraper.gem_fetcher import GemFetcher
from scraper.result_fetcher import ResultFetcher
from scraper.parser import Parser
from scraper.evaluation_parser import EvaluationParser

from processing.data_cleaner import DataCleaner
from processing.insights import Insights


logger = setup_logger()


def main():

    parser = argparse.ArgumentParser(
        description="GemEdge Procurement Intelligence Scraper",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:

python main.py --fetch
python main.py --parse
python main.py --fetch --limit 50
"""
    )

    # Fetch mode
    parser.add_argument(
        "--fetch",
        action="store_true",
        help="Fetch HTML and save locally"
    )

    # Parse mode
    parser.add_argument(
        "--parse",
        action="store_true",
        help="Parse saved HTML"
    )

    # Optional limit
    parser.add_argument(
        "--limit",
        type=int,
        default=30,
        help="Number of entries"
    )

    args = parser.parse_args()

    # -------------------------------------
    # Validation
    # -------------------------------------

    if not args.fetch and not args.parse:

        logger.error(
            "Specify either --fetch or --parse"
        )

        parser.print_help()

        sys.exit(1)

    if args.fetch and args.parse:

        logger.error(
            "Cannot use both --fetch and --parse"
        )

        sys.exit(1)

    # -------------------------------------
    # Create folders
    # -------------------------------------

    FileManager.ensure_directories()

    # =====================================
    # FETCH MODE
    # =====================================

    if args.fetch:

        logger.info("=" * 60)
        logger.info("MODE: FETCH")
        logger.info(
            f"Target entries: {args.limit}"
        )
        logger.info("=" * 60)

        try:

            # --------------------------
            # STEP 1
            # --------------------------

            logger.info(
                "STEP 1: Fetch listing pages"
            )

            fetcher = GemFetcher()

            fetcher.fetch()

            logger.info(
                "Listing pages fetched"
            )

            # --------------------------
            # STEP 2
            # --------------------------

            logger.info(
                "STEP 2: Fetch result pages"
            )

            result_fetcher = (
                ResultFetcher()
            )

            result_fetcher.fetch_results()

            logger.info(
                "Result pages fetched"
            )

            logger.info(
                "Fetch completed successfully"
            )

        except Exception as e:

            logger.error(
                f"Fetch failed: {e}"
            )

            sys.exit(1)

    # =====================================
    # PARSE MODE
    # =====================================

    elif args.parse:

        logger.info("=" * 60)
        logger.info("MODE: PARSE")
        logger.info("=" * 60)

        try:

            final_data = []

            # --------------------------
            # Parse listing pages
            # --------------------------

            listing_data = (
                Parser.parse_all()
            )

            logger.info(
                f"Listing records: {len(listing_data)}"
            )

            final_data.extend(
                listing_data
            )

            # --------------------------
            # Parse evaluation pages
            # --------------------------

            evaluation_data = (
                EvaluationParser.parse_all()
            )

            logger.info(
                f"Evaluation records: {len(evaluation_data)}"
            )

            final_data.extend(
                evaluation_data
            )

            # --------------------------
            # Convert to DataFrame
            # --------------------------

            df = pd.DataFrame(
                final_data
            )

            # --------------------------
            # Clean data
            # --------------------------

            logger.info(
                "Cleaning data..."
            )

            df = DataCleaner.process(
                df
            )

            # --------------------------
            # Save output
            # --------------------------

            logger.info(
                "Saving output files..."
            )

            DataSaver.save(
                df.to_dict(
                    orient="records"
                )
            )

            # --------------------------
            # Generate insights
            # --------------------------

            Insights.generate(
                df
            )

            logger.info(
                f"Final records: {len(df)}"
            )

            logger.info(
                "Parse completed successfully"
            )

        except Exception as e:

            logger.error(
                f"Parse failed: {e}"
            )

            sys.exit(1)


if __name__ == "__main__":
    main()