"""
Fetch result pages from extracted result links
"""

from scraper.browser_manager import BrowserManager
from scraper.parser import Parser
from utils.file_manager import FileManager
from utils.logger import setup_logger

from config import (
    EVALUATIONS_DIR
)

logger = setup_logger()


class ResultFetcher:

    def __init__(self):

        self.logger = logger

        parser = Parser()

        self.records = (
            parser.parse_all_listing_pages()
        )

    def fetch_results(self):

        self.logger.info(
            f"Found {len(self.records)} records"
        )

        with BrowserManager() as page:

            count = 0

            for record in self.records:

                result_link = record.get(
                    "result_link"
                )

                bid_id = record.get(
                    "bid_id"
                )

                if not result_link:

                    continue

                try:

                    # convert relative url to full url
                    full_url = (
                        "https://bidplus.gem.gov.in"
                        + result_link
                    )

                    self.logger.info(
                        f"Opening {bid_id}"
                    )

                    page.goto(
                        full_url,
                        wait_until="networkidle"
                    )

                    page.wait_for_timeout(
                        3000
                    )

                    html = page.content()

                    filename = (
                        f"{bid_id.replace('/','_')}.html"
                    )

                    FileManager.save_html(
                        html,
                        filename,
                        EVALUATIONS_DIR
                    )

                    count += 1

                except Exception as e:

                    self.logger.error(
                        f"Failed for {bid_id}: {e}"
                    )

        self.logger.info(
            f"Saved {count} result pages"
        )