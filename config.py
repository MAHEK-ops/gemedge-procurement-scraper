# config.py
"""
Configuration file for GemEdge scraper
"""

import os

# Target URL
BASE_URL = "https://bidplus.gem.gov.in/all-bids"

# Filter settings
FILTERS = {
    "status": "Bid/RA",
    "outcome": "Awarded"
}

# Scraping settings
MIN_ENTRIES = 30
START_PAGE = 1
END_PAGE = 5
MAX_RETRIES = 3

# Timeouts (milliseconds)
TIMEOUT = 30000
WAIT_AFTER_CLICK = 2000

# Browser settings
HEADLESS = True

# Directory structure
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

RAW_HTML_DIR = os.path.join(BASE_DIR, "raw_html")
LISTINGS_DIR = os.path.join(RAW_HTML_DIR, "listings")
BID_DETAILS_DIR = os.path.join(RAW_HTML_DIR, "bid_details")
EVALUATIONS_DIR = os.path.join(RAW_HTML_DIR, "evaluations")

OUTPUT_DIR = os.path.join(BASE_DIR, "output")

CSV_FILE = os.path.join(
    OUTPUT_DIR,
    "procurement_data.csv"
)

JSON_FILE = os.path.join(
    OUTPUT_DIR,
    "procurement_data.json"
)