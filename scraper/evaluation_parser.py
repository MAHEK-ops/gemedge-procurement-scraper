from bs4 import BeautifulSoup
import re

from utils.logger import setup_logger
from utils.file_manager import FileManager
from config import EVALUATIONS_DIR

logger = setup_logger()


class EvaluationParser:

    @staticmethod
    def parse(html):

        soup = BeautifulSoup(
            html,
            "html.parser"
        )

        tables = soup.find_all(
            "table"
        )

        if not tables:

            logger.warning(
                "No tables found"
            )

            return []

        results = []

        for table in tables:

            header_row = table.find(
                "tr"
            )

            if not header_row:
                continue

            headers = []

            for th in header_row.find_all(
                ["th", "td"]
            ):

                text = th.get_text(
                    " ",
                    strip=True
                )

                headers.append(
                    text
                )

            headers_text = " ".join(
                headers
            )

            headers_text = re.sub(
                r"\s+",
                " ",
                headers_text
            ).lower()

            # -------------------------
            # FINANCIAL TABLE
            # -------------------------

            if "total price" in headers_text:

                logger.info(
                    "Financial table detected"
                )

                rows = table.find_all(
                    "tr"
                )[1:]

                for row in rows:

                    cols = row.find_all(
                        "td"
                    )

                    if len(cols) < 5:
                        continue

                    results.append({

                        "evaluation_type":
                        "financial",

                        "seller_name":
                        cols[1].get_text(
                            " ",
                            strip=True
                        )
                        .replace(
                            "Under PMA",
                            ""
                        )
                        .strip(),

                        "offered_item":
                        cols[2].get_text(
                            " ",
                            strip=True
                        ),

                        "total_price":
                        cols[3].get_text(
                            " ",
                            strip=True
                        ),

                        "rank":
                        cols[4].get_text(
                            " ",
                            strip=True
                        )
                    })

            # -------------------------
            # TECHNICAL TABLE
            # -------------------------

            elif (
                "participated on"
                in headers_text
            ):

                logger.info(
                    "Technical table detected"
                )

                rows = table.find_all(
                    "tr"
                )[1:]

                for row in rows:

                    cols = row.find_all(
                        "td"
                    )

                    if len(cols) < 6:
                        continue

                    results.append({

                        "evaluation_type":
                        "technical",

                        "seller_name":
                        cols[1].get_text(
                            " ",
                            strip=True
                        )
                        .replace(
                            "Under PMA",
                            ""
                        )
                        .strip(),

                        "participated_on":
                        cols[3].get_text(
                            " ",
                            strip=True
                        ),

                        "status":
                        cols[-1].get_text(
                            " ",
                            strip=True
                        )
                    })

        return results


    @staticmethod
    def parse_all():

        all_records = []

        files = FileManager.list_html_files(
            EVALUATIONS_DIR
        )

        logger.info(
            f"Found {len(files)} evaluation files"
        )

        for file in files:

            html = FileManager.load_html(
                file,
                EVALUATIONS_DIR
            )

            if not html:
                continue

            records = EvaluationParser.parse(
                html
            )

            logger.info(
                f"{file}: {len(records)} records"
            )

            all_records.extend(
                records
            )

        return all_records