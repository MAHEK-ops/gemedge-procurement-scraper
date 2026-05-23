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

from config import EVALUATIONS_DIR


logger = setup_logger()


def main():

    parser = argparse.ArgumentParser(
        description="GemEdge Procurement Intelligence Scraper"
    )

    parser.add_argument(
        "--fetch",
        action="store_true"
    )

    parser.add_argument(
        "--parse",
        action="store_true"
    )

    parser.add_argument(
        "--limit",
        type=int,
        default=30
    )

    args = parser.parse_args()

    # -------------------------
    # validation
    # -------------------------

    if not args.fetch and not args.parse:

        logger.error(
            "Specify --fetch or --parse"
        )

        sys.exit(1)

    if args.fetch and args.parse:

        logger.error(
            "Cannot use both modes"
        )

        sys.exit(1)

    FileManager.ensure_directories()

    # ==================================================
    # FETCH
    # ==================================================

    if args.fetch:

        logger.info("="*60)
        logger.info("MODE: FETCH")
        logger.info("="*60)

        try:

            logger.info(
                "STEP 1: Fetch listing pages"
            )

            fetcher = GemFetcher()

            fetcher.fetch()

            logger.info(
                "STEP 2: Fetch result pages"
            )

            result_fetcher = (
                ResultFetcher()
            )

            result_fetcher.fetch_results()

            logger.info(
                "Fetch completed"
            )

        except Exception as e:

            logger.error(
                f"Fetch failed: {e}"
            )

            sys.exit(1)

    # ==================================================
    # PARSE
    # ==================================================

    elif args.parse:

        logger.info("="*60)
        logger.info("MODE: PARSE")
        logger.info("="*60)

        try:

            all_records=[]

            # -------------------------
            # Listing pages
            # -------------------------

            listing_records=(
                Parser.parse_all()
            )

            logger.info(
                f"Listing records: {len(listing_records)}"
            )

            all_records.extend(
                listing_records
            )

            # -------------------------
            # Evaluation pages
            # -------------------------

            files=(
                FileManager.list_html_files(
                    EVALUATIONS_DIR
                )
            )

            evaluation_records=[]

            logger.info(
                f"Found {len(files)} evaluation files"
            )

            for file in files:

                html=(
                    FileManager.load_html(
                        file,
                        EVALUATIONS_DIR
                    )
                )

                if not html:
                    continue

                records=(
                    EvaluationParser.parse(
                        html
                    )
                )

                # attach bid_id
                bid_id=(
                    file
                    .replace(".html","")
                    .replace("_","/")
                )

                for row in records:

                    row["bid_id"]=bid_id

                    evaluation_records.append(
                        row
                    )

                logger.info(
                    f"{file}: {len(records)} records"
                )

            logger.info(
                f"Evaluation records: {len(evaluation_records)}"
            )

            all_records.extend(
                evaluation_records
            )

            # -------------------------
            # Dataframe
            # -------------------------

            df=pd.DataFrame(
                all_records
            )

            logger.info(
                "Cleaning data..."
            )

            df=DataCleaner.process(
                df
            )

            logger.info(
                "Saving output files..."
            )

            DataSaver.save(
                df.to_dict(
                    orient="records"
                )
            )

            # -------------------------
            # Insights
            # -------------------------

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


if __name__=="__main__":
    main()