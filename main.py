"""
Main entry point for GemEdge scraper
Supports two modes:
--fetch : Fetch listing pages + result pages
--parse : Parse saved HTML
"""

import argparse
import sys

from utils.logger import setup_logger
from utils.file_manager import FileManager

from scraper.gem_fetcher import GemFetcher
from scraper.result_fetcher import ResultFetcher

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

    # ---------------------------
    # Validation
    # ---------------------------

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

    # ---------------------------
    # Create folders
    # ---------------------------

    FileManager.ensure_directories()

    # ---------------------------
    # FETCH MODE
    # ---------------------------

    if args.fetch:

        logger.info("=" * 60)
        logger.info("MODE: FETCH")
        logger.info(
            f"Target entries: {args.limit}"
        )
        logger.info("=" * 60)

        try:

            # Step 1:
            # Fetch listing pages

            logger.info(
                "STEP 1: Fetch listing pages"
            )

            fetcher = GemFetcher()

            fetcher.fetch()

            logger.info(
                "Listing pages fetched"
            )

            # Step 2:
            # Fetch result pages

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

    # ---------------------------
    # PARSE MODE
    # ---------------------------

    elif args.parse:

        logger.info("=" * 60)
        logger.info("MODE: PARSE")
        logger.info("=" * 60)

        try:

            logger.info(
                "Parser integration pending"
            )

        except Exception as e:

            logger.error(
                f"Parse failed: {e}"
            )

            sys.exit(1)


if __name__ == "__main__":
    main()