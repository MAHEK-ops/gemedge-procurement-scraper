"""
Fetches GeM listing pages and saves raw HTML
"""

from scraper.browser_manager import BrowserManager
from utils.logger import setup_logger
from utils.file_manager import FileManager

from config import (
    BASE_URL,
    FILTERS,
    LISTINGS_DIR,
    START_PAGE,
    END_PAGE
)

logger = setup_logger()


class GemFetcher:

    def __init__(self):
        self.logger = logger

    def apply_filters(self, page):
        """
        Apply required GeM filters
        """

        try:
            self.logger.info("Applying filters")

            # Click Bid/RA Status
            page.locator("#bidrastatus").check()

            page.wait_for_timeout(1000)

            # Click Bid / RA Awarded
            page.locator("#bid_awarded").check()

            page.wait_for_timeout(2000)

            self.logger.info("Filters applied")

        except Exception as e:
            self.logger.error(
                f"Filter application failed: {e}"
            )
            raise

    def go_to_next_page(self, page):
        """
        Navigate to next pagination page
        """

        try:

            self.logger.info(
                f"Current page URL: {page.url}"
            )

            next_button = page.locator(
                "a.page-link.next"
            )

            if next_button.count() > 0:

                self.logger.info(
                    "Clicking next page..."
                )

                next_button.click()

                page.wait_for_timeout(3000)

                page.wait_for_load_state(
                    "networkidle"
                )

                self.logger.info(
                    "Moved to next page"
                )

                return True

            else:

                self.logger.warning(
                    "No next button found"
                )

                return False

        except Exception as e:

            self.logger.error(
                f"Pagination failed: {e}"
            )

            return False

    def fetch(self):
        """
        Main fetch process
        """

        self.logger.info(
            "Starting GeM fetch process"
        )

        with BrowserManager() as page:

            page.goto(
                BASE_URL,
                wait_until="networkidle"
            )

            self.logger.info(
                "Website loaded"
            )

            self.apply_filters(page)

            for page_num in range(
                START_PAGE,
                END_PAGE + 1
            ):

                self.logger.info(
                    f"Processing page {page_num}"
                )

                html = page.content()

                FileManager.save_html(
                    html,
                    f"listing_page_{page_num}.html",
                    LISTINGS_DIR
                )

                if page_num < END_PAGE:

                    success = self.go_to_next_page(
                        page
                    )

                    if not success:
                        break

        self.logger.info(
            "Listing pages fetched successfully"
        )