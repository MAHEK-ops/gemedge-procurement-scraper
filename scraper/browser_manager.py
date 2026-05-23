"""
Manages Playwright browser lifecycle
Handles browser startup, page creation, and cleanup
"""

from playwright.sync_api import sync_playwright, Browser, Page
from utils.logger import setup_logger

logger = setup_logger()

class BrowserManager:
    """
    Context manager for Playwright browser
    Ensures proper cleanup even if errors occur
    """
    
    def __init__(self, headless=True):
        """
        Initialize browser manager
        
        Args:
            headless (bool): Run browser without UI (True for production, False for debugging)
        """
        self.headless = headless
        self.playwright = None
        self.browser = None
        self.context = None
        self.page = None
    
    def __enter__(self):
        """
        Called when entering 'with' block
        Starts browser and returns page object
        """
        logger.info("Starting Playwright browser...")
        
        # Start Playwright
        self.playwright = sync_playwright().start()
        
        # Launch browser (Chromium by default)
        self.browser = self.playwright.chromium.launch(
            headless=self.headless,
            args=['--no-sandbox']  # Required for some environments
        )
        
        # Create browser context (like an incognito window)
        self.context = self.browser.new_context(
            viewport={'width': 1920, 'height': 1080},  # Desktop resolution
            user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'  # Mimic real browser
        )
        
        # Create new page (tab)
        self.page = self.context.new_page()
        
        logger.info("Browser ready!")
        return self.page
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        Called when exiting 'with' block
        Cleans up browser resources
        """
        logger.info("Closing browser...")
        
        if self.page:
            self.page.close()
        if self.context:
            self.context.close()
        if self.browser:
            self.browser.close()
        if self.playwright:
            self.playwright.stop()
        
        logger.info("Browser closed successfully")