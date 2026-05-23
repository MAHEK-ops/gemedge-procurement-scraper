"""
Parses saved GeM listing HTML files
Extracts structured bid information
"""

from bs4 import BeautifulSoup

from utils.logger import setup_logger
from utils.file_manager import FileManager
from config import LISTINGS_DIR

logger = setup_logger()


class GemParser:

    def __init__(self):
        self.logger = logger

    def parse_all_listing_pages(self):
        """
        Parse all HTML files from listings directory
        """

        all_records = []

        html_files = FileManager.list_html_files(
            LISTINGS_DIR
        )

        self.logger.info(
            f"Found {len(html_files)} files"
        )

        for file in html_files:

            self.logger.info(
                f"Parsing {file}"
            )

            html = FileManager.load_html(
                file,
                LISTINGS_DIR
            )

            if html:

                records = self.parse_listing_page(
                    html
                )

                all_records.extend(
                    records
                )

        return all_records


    def parse_listing_page(self, html):
        """
        Parse a single listing page HTML
        """

        records = []

        soup = BeautifulSoup(
            html,
            "html.parser"
        )

        cards = soup.select(
            "#bidCard .card"
        )

        self.logger.info(
            f"Found {len(cards)} bid cards"
        )

        for card in cards:

            try:

                record = {}

                # ========================
                # Bid ID and RA Number
                # ========================

                bid_links = card.select(
                    ".bid_no_hover"
                )

                if len(bid_links) > 0:

                    record["bid_id"] = (
                        bid_links[0]
                        .text.strip()
                    )

                else:

                    record["bid_id"] = None


                if len(bid_links) > 1:

                    record["ra_no"] = (
                        bid_links[1]
                        .text.strip()
                    )

                else:

                    record["ra_no"] = None


                # ========================
                # Item
                # ========================

                item = card.select_one(
                    'a[data-toggle="popover"]'
                )

                if item:

                    record["item"] = (
                        item.text.strip()
                    )

                else:

                    record["item"] = None


                # ========================
                # Quantity
                # ========================

                quantity = None

                quantity_divs = card.select(
                    ".col-md-4 .row"
                )

                for row in quantity_divs:

                    text = row.get_text(
                        " ",
                        strip=True
                    )

                    if "Quantity:" in text:

                        quantity = (
                            text.replace(
                                "Quantity:",
                                ""
                            )
                            .strip()
                        )

                        break

                record["quantity"] = quantity


                # ========================
                # Department
                # ========================

                department_rows = card.select(
                    ".col-md-5 .row"
                )

                if len(department_rows) > 1:

                    department = (
                        department_rows[1]
                        .get_text(
                            separator=" | ",
                            strip=True
                        )
                    )

                    record["department"] = (
                        department
                    )

                else:

                    record["department"] = None


                # ========================
                # Start Date
                # ========================

                start = card.select_one(
                    ".start_date"
                )

                record["start_date"] = (
                    start.text.strip()
                    if start
                    else None
                )


                # ========================
                # End Date
                # ========================

                end = card.select_one(
                    ".end_date"
                )

                record["end_date"] = (
                    end.text.strip()
                    if end
                    else None
                )


                # ========================
                # Result Link
                # ========================

                result = card.select_one(
                    'a[href*="ResultView"]'
                )

                if result:

                    record["result_link"] = (
                        result["href"]
                    )

                else:

                    record["result_link"] = None


                records.append(
                    record
                )


            except Exception as e:

                self.logger.error(
                    f"Card parsing failed: {e}"
                )

        return records