"""
Main entry point for the betting bot application.
"""
import sys
import time
from datetime import datetime
from pathlib import Path

# Add project root to Python path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.api.sharpxch_client import SharpXchClient
from src.utils.data_manager import DataManager
from src.utils.logger import logger
from src.utils.config import API_USERNAME, API_PASSWORD


def main():
    """Main function to run the betting bot."""
    logger.info("Starting betting bot application")
    
    try:
        # Create API client
        client = SharpXchClient()
        logger.info(f"Created SharpXch client with username: {API_USERNAME}")
        
        # Create data manager
        data_manager = DataManager()
        
        # Test login
        logger.info("Testing API login...")
        login_success = client.login()
        
        if not login_success:
            logger.error("Failed to login to SharpXch API. Please check credentials.")
            return 1
        
        logger.success("Successfully logged in to SharpXch API")
        
        # Get matches for today
        today = datetime.now().strftime("%Y-%m-%d")
        logger.info(f"Fetching matches for {today}...")
        
        matches_response = client.get_matches(date=today)
        
        logger.info(f"Retrieved {len(matches_response.matches)} matches for {today}")
        
        # Save matches to file
        data_manager.save_matches(matches_response.matches)
        
        # Get markets for each match and save them
        for match in matches_response.matches:
            logger.info(f"Fetching markets for match: {match.home_team} vs {match.away_team}")
            
            try:
                markets_response = client.get_match_markets(match.id)
                data_manager.save_match_markets(match.id, markets_response.markets)
                
                # Add a small delay to avoid overwhelming the API
                time.sleep(0.5)
                
            except Exception as e:
                logger.error(f"Failed to fetch markets for match {match.id}: {e}")
        
        # Export matches to CSV
        csv_path = data_manager.export_matches_to_csv()
        if csv_path:
            logger.info(f"Matches exported to CSV: {csv_path}")
        
        logger.success("Betting bot completed successfully")
        return 0
        
    except Exception as e:
        logger.error(f"An error occurred: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
