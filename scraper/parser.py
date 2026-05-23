from bs4 import BeautifulSoup
import re

from utils.file_manager import FileManager
from utils.logger import setup_logger
from config import LISTINGS_DIR

logger = setup_logger()


class Parser:

    @staticmethod
    def parse_listing(html):

        soup = BeautifulSoup(
            html,
            "html.parser"
        )

        cards = soup.find_all(
            "div",
            class_="card"
        )

        logger.info(
            f"Found {len(cards)} bid cards"
        )

        records=[]

        for card in cards:

            try:

                text=card.get_text(
                    " ",
                    strip=True
                )

                bid_id="N/A"
                ra_no="N/A"
                item="N/A"
                category="N/A"
                quantity="N/A"
                department="N/A"
                buyer="N/A"
                start_date="N/A"
                end_date="N/A"
                result_link="N/A"

                # -------------------------
                # Bid ID
                # -------------------------

                bid_match=re.search(
                    r"GEM/\d+/B/\d+",
                    text
                )

                if bid_match:
                    bid_id=bid_match.group()

                ra_match=re.search(
                    r"GEM/\d+/R/\d+",
                    text
                )

                if ra_match:
                    ra_no=ra_match.group()


                # -------------------------
                # Item name
                # -------------------------

                p_tags=card.find_all("p")

                for p in p_tags:

                    value=p.get_text(
                        " ",
                        strip=True
                    )

                    if (
                        "BID NO" not in value
                        and
                        "RA NO" not in value
                        and
                        len(value)>10
                    ):

                        item=value
                        break


                # -------------------------
                # Category
                # -------------------------

                category_tag=card.find(
                    string=lambda x:
                    x and
                    "Category" in x
                )

                if category_tag:

                    category=(
                        category_tag
                        .replace(
                            "Category:",
                            ""
                        )
                        .strip()
                    )


                # -------------------------
                # Quantity
                # -------------------------

                qty_match=re.search(
                    r"Quantity[:\s]*(\d+)",
                    text
                )

                if qty_match:
                    quantity=qty_match.group(1)


                # -------------------------
                # Department
                # -------------------------

                ministry_match=re.search(
                    r"(Ministry.*?)(?=Start Date|End Date|Quantity|$)",
                    text
                )

                if ministry_match:

                    department=(
                        ministry_match
                        .group(1)
                        .strip()
                    )

                    buyer=department


                # -------------------------
                # Result link
                # -------------------------

                button=card.find(
                    "a",
                    string=lambda x:
                    x and
                    "Result" in x
                )

                if button:

                    result_link=button.get(
                        "href",
                        "N/A"
                    )


                records.append({

                    "bid_id":bid_id,
                    "ra_no":ra_no,
                    "category":category,
                    "item":item,
                    "buyer":buyer,
                    "department":department,
                    "quantity":quantity,
                    "result_link":result_link
                })

            except Exception as e:

                logger.warning(
                    f"Card error: {e}"
                )

        return records


    @staticmethod
    def parse_all():

        all_records=[]

        files=FileManager.list_html_files(
            LISTINGS_DIR
        )

        logger.info(
            f"Found {len(files)} files"
        )

        for file in files:

            logger.info(
                f"Parsing {file}"
            )

            html=FileManager.load_html(
                file,
                LISTINGS_DIR
            )

            if html:

                records=(
                    Parser.parse_listing(
                        html
                    )
                )

                all_records.extend(
                    records
                )

        return all_records