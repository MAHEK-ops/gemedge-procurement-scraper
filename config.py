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

# Scraping limits
MIN_ENTRIES = 30

# Timeouts (in milliseconds)
TIMEOUT = 30000
WAIT_AFTER_CLICK = 2000

# Directory structure
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
RAW_HTML_DIR = os.path.join(BASE_DIR, "raw_html")
LISTINGS_DIR = os.path.join(RAW_HTML_DIR, "listings")
BID_DETAILS_DIR = os.path.join(RAW_HTML_DIR, "bid_details")
EVALUATIONS_DIR = os.path.join(RAW_HTML_DIR, "evaluations")

OUTPUT_DIR = os.path.join(BASE_DIR, "output")
CSV_FILE = os.path.join(OUTPUT_DIR, "procurement_data.csv")
JSON_FILE = os.path.join(OUTPUT_DIR, "procurement_data.json")

# Browser settings
HEADLESS = True  # Set to False for debugging