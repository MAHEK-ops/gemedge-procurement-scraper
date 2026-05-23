"""
Test script to verify setup
"""

from scraper.browser_manager import BrowserManager
from utils.file_manager import FileManager
from config import BASE_URL, LISTINGS_DIR
from utils.logger import setup_logger

logger = setup_logger()

def test_fetch_and_save():
    """
    Test: Navigate to GemEdge and save homepage HTML
    """
    logger.info("Starting fetch test...")
    
    # Ensure directories exist
    FileManager.ensure_directories()
    
    with BrowserManager(headless=False) as page:
        logger.info(f"Navigating to {BASE_URL}")
        page.goto(BASE_URL, wait_until="domcontentloaded")
        
        # Wait for page to load
        page.wait_for_timeout(3000)
        
        # Get page HTML
        html_content = page.content()
        
        # Save to file
        FileManager.save_html(
            content=html_content,
            filename="test_homepage.html",
            directory=LISTINGS_DIR
        )
        
        logger.info(f"Page title: {page.title()}")
        logger.info("HTML saved successfully!")

if __name__ == "__main__":
    test_fetch_and_save()