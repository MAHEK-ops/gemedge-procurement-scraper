"""
Manages file operations for saving/loading HTML
"""

import os
import json
from datetime import datetime
from utils.logger import setup_logger

logger = setup_logger()

class FileManager:
    """
    Handles saving and loading of raw HTML files
    """
    
    @staticmethod
    def ensure_directories():
        """
        Create necessary directories if they don't exist
        """
        from config import (RAW_HTML_DIR, LISTINGS_DIR, 
                          BID_DETAILS_DIR, EVALUATIONS_DIR, OUTPUT_DIR)
        
        directories = [
            RAW_HTML_DIR,
            LISTINGS_DIR,
            BID_DETAILS_DIR,
            EVALUATIONS_DIR,
            OUTPUT_DIR
        ]
        
        for directory in directories:
            os.makedirs(directory, exist_ok=True)
            logger.debug(f"Ensured directory exists: {directory}")
    
    @staticmethod
    def save_html(content, filename, directory):
        """
        Save HTML content to file
        
        Args:
            content (str): HTML content
            filename (str): File name (e.g., 'listing_page_1.html')
            directory (str): Target directory path
        
        Returns:
            str: Full path of saved file
        """
        filepath = os.path.join(directory, filename)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        
        logger.info(f"Saved HTML: {filepath}")
        return filepath
    
    @staticmethod
    def load_html(filename, directory):
        """
        Load HTML content from file
        
        Args:
            filename (str): File name
            directory (str): Source directory
        
        Returns:
            str: HTML content or None if file doesn't exist
        """
        filepath = os.path.join(directory, filename)
        
        if not os.path.exists(filepath):
            logger.warning(f"File not found: {filepath}")
            return None
        
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        logger.debug(f"Loaded HTML: {filepath}")
        return content
    
    @staticmethod
    def list_html_files(directory):
        """
        List all HTML files in a directory
        
        Args:
            directory (str): Directory to search
        
        Returns:
            list: List of HTML filenames
        """
        if not os.path.exists(directory):
            return []
        
        files = [f for f in os.listdir(directory) if f.endswith('.html')]
        logger.debug(f"Found {len(files)} HTML files in {directory}")
        return sorted(files)
    
    @staticmethod
    def save_metadata(data, filename="fetch_metadata.json"):
        """
        Save metadata about the fetch operation
        (e.g., timestamp, number of entries fetched)
        
        Args:
            data (dict): Metadata to save
            filename (str): Metadata filename
        """
        from config import RAW_HTML_DIR
        
        filepath = os.path.join(RAW_HTML_DIR, filename)
        
        # Add timestamp
        data['fetch_timestamp'] = datetime.now().isoformat()
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, indent=2, fp=f)
        
        logger.info(f"Saved metadata: {filepath}")