"""
Simple logging utility for debugging
Helps track scraper progress and errors
"""

import logging
from datetime import datetime

def setup_logger(name="gemedge_scraper"):
    """
    Creates a logger that writes to both console and file
    
    Args:
        name (str): Logger name
    
    Returns:
        logging.Logger: Configured logger instance
    """
    # Create logger
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)  # Capture INFO level and above
    
    # Avoid duplicate handlers if logger already exists
    if logger.handlers:
        return logger
    
    # Console handler (prints to terminal)
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    
    # File handler (saves to file)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    file_handler = logging.FileHandler(f"scraper_{timestamp}.log")
    file_handler.setLevel(logging.DEBUG)  # Save more detailed logs to file
    
    # Format: [2024-05-23 12:30:45] INFO: Message
    formatter = logging.Formatter(
        '[%(asctime)s] %(levelname)s: %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    console_handler.setFormatter(formatter)
    file_handler.setFormatter(formatter)
    
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)
    
    return logger