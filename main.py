"""
Main entry point for GemEdge scraper
Supports two modes: --fetch and --parse
"""

import argparse
import sys
from utils.logger import setup_logger
from utils.file_manager import FileManager

logger = setup_logger()

def main():
    """
    Parse command-line arguments and execute appropriate mode
    """
    # Create argument parser
    parser = argparse.ArgumentParser(
        description='GemEdge Procurement Intelligence Scraper',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Fetch HTML from website (run once)
  python main.py --fetch
  
  # Parse saved HTML files
  python main.py --parse
  
  # Fetch with custom entry limit
  python main.py --fetch --limit 50
        """
    )
    
    # Add arguments
    parser.add_argument(
        '--fetch',
        action='store_true',
        help='Fetch HTML from website and save locally'
    )
    
    parser.add_argument(
        '--parse',
        action='store_true',
        help='Parse saved HTML files and generate output'
    )
    
    parser.add_argument(
        '--limit',
        type=int,
        default=30,
        help='Number of bid entries to fetch (default: 30)'
    )
    
    # Parse arguments
    args = parser.parse_args()
    
    # Validate: must specify either --fetch or --parse
    if not args.fetch and not args.parse:
        logger.error("Must specify either --fetch or --parse")
        parser.print_help()
        sys.exit(1)
    
    if args.fetch and args.parse:
        logger.error("Cannot use --fetch and --parse together")
        sys.exit(1)
    
    # Ensure directories exist
    FileManager.ensure_directories()
    
    # Execute appropriate mode
    if args.fetch:
        logger.info("=" * 60)
        logger.info("MODE: FETCH")
        logger.info(f"Target: {args.limit} entries")
        logger.info("=" * 60)
        
        # TODO: Import and run fetcher
        logger.info("Fetcher not implemented yet")
        # from scraper.fetcher import run_fetch
        # run_fetch(limit=args.limit)
    
    elif args.parse:
        logger.info("=" * 60)
        logger.info("MODE: PARSE")
        logger.info("=" * 60)
        
        # TODO: Import and run parser
        logger.info("Parser not implemented yet")
        # from scraper.parser import run_parse
        # run_parse()

if __name__ == "__main__":
    main()