from bs4 import BeautifulSoup
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

        records = []

        for card in cards:

            try:

                bid_id = None
                ra_no = None
                item = None
                quantity = None
                department = None
                start_date = None
                end_date = None
                result_link = None

                text = card.get_text(
                    " ",
                    strip=True
                )

                # Bid ID
                if "GEM/" in text:

                    for word in text.split():

                        if "GEM/" in word:

                            if "/B/" in word:
                                bid_id = word

                            elif "/R/" in word:
                                ra_no = word

                # Item
                item_tag = card.find("p")

                if item_tag:
                    item = item_tag.get_text(
                        strip=True
                    )

                # Result link
                result_button = card.find(
                    "a",
                    string=lambda x:
                    x and "Result" in x
                )

                if result_button:

                    result_link = (
                        result_button.get(
                            "href"
                        )
                    )

                records.append({

                    "bid_id": bid_id,
                    "ra_no": ra_no,
                    "item": item,
                    "quantity": quantity,
                    "department": department,
                    "start_date": start_date,
                    "end_date": end_date,
                    "result_link": result_link

                })

            except Exception as e:

                logger.warning(
                    f"Error parsing card: {e}"
                )

        return records


    @staticmethod
    def parse_all():

        all_records = []

        files = (
            FileManager.list_html_files(
                LISTINGS_DIR
            )
        )

        logger.info(
            f"Found {len(files)} files"
        )

        for file in files:

            logger.info(
                f"Parsing {file}"
            )

            html = (
                FileManager.load_html(
                    file,
                    LISTINGS_DIR
                )
            )

            if html:

                records = (
                    Parser.parse_listing(
                        html
                    )
                )

                all_records.extend(
                    records
                )

        return all_records