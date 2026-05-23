"""
Main entry point for GemEdge scraper
Supports two modes: --fetch and --parse
"""

import argparse
import sys

from utils.logger import setup_logger
from utils.file_manager import FileManager
from scraper.gem_fetcher import GemFetcher

logger = setup_logger()


def main():
    """
    Parse command-line arguments and execute mode
    """

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
        help="Parse saved HTML files"
    )

    # Limit entries
    parser.add_argument(
        "--limit",
        type=int,
        default=30,
        help="Number of entries to fetch"
    )

    args = parser.parse_args()

    # Validation

    if not args.fetch and not args.parse:

        logger.error(
            "Please specify either --fetch or --parse"
        )

        parser.print_help()

        sys.exit(1)

    if args.fetch and args.parse:

        logger.error(
            "Cannot use --fetch and --parse together"
        )

        sys.exit(1)

    # Create directories if missing

    FileManager.ensure_directories()

    # FETCH MODE

    if args.fetch:

        logger.info("=" * 60)
        logger.info("MODE: FETCH")
        logger.info(
            f"Target entries: {args.limit}"
        )
        logger.info("=" * 60)

        try:

            fetcher = GemFetcher()

            fetcher.fetch()

            logger.info(
                "Fetch completed successfully"
            )

        except Exception as e:

            logger.error(
                f"Fetch failed: {e}"
            )

            sys.exit(1)

    # PARSE MODE

    elif args.parse:

        logger.info("=" * 60)
        logger.info("MODE: PARSE")
        logger.info("=" * 60)

        try:

            logger.info(
                "Parser not implemented yet"
            )

            # future:
            # parser = GemParser()
            # parser.parse()

        except Exception as e:

            logger.error(
                f"Parse failed: {e}"
            )

            sys.exit(1)


if __name__ == "__main__":
    main()