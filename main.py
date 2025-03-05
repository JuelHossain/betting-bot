"""
SharpXch Betting Bot - Main Entry Point

This is the main entry point for the SharpXch betting bot.
It handles authentication, data retrieval, and bet placement
based on configured strategies.
"""
import logging
import os
import sys
from datetime import datetime
from pathlib import Path

# Set up basic logging
LOG_DIR = os.path.join(Path(__file__).parent, "logs")
os.makedirs(LOG_DIR, exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler(os.path.join(LOG_DIR, f"betting_bot_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"))
    ]
)

# Import modules
from src.api.sharpxch_client import SharpXchClient
from src.utils.config import API_BASE_URL, API_USERNAME, API_PASSWORD, AUTH_ENDPOINT


def main():
    """Main entry point for the betting bot."""
    print("\n=== SharpXch Betting Bot ===")
    print("Version 1.0.0\n")

    # Initialize API client
    print("Initializing API client...")
    client = SharpXchClient(
        base_url=API_BASE_URL,
        username=API_USERNAME,
        password=API_PASSWORD,
        auth_endpoint=AUTH_ENDPOINT,
        save_responses=True  # Enable response saving
    )

    # Step 1: Authenticate
    print("\nStep 1: Authenticating with SharpXch API...")
    if not client.login():
        print("❌ Authentication failed! Check your credentials and network connection.")
        return 1

    print("✅ Authentication successful!")
    print(f"Token expires at: {client.token_expiry}")

    # Step 2: Get user profile
    print("\nStep 2: Retrieving user profile information...")
    try:
        profile = client.get_profile()
        print("✅ Profile retrieved successfully!")

        print("\n=== User Profile Summary ===")
        print(f"Username: {profile.get('username', 'N/A')}")
        print(f"Available Balance: {profile.get('availableToBet', 'N/A')} {profile.get('currency', [''])[0]}")
        print(f"Account Since: {profile.get('joinedDate', 'N/A')}")
        print("============================")

    except Exception as e:
        print(f"❌ Profile retrieval failed: {e}")
        return 1

    # Step 3: Get sports data
    print("\nStep 3: Retrieving sports data...")
    try:
        sports_data = client.get_sport_details()
        sports_count = len(sports_data.get("content", []))
        print(f"✅ Sports data retrieved successfully! Found {sports_count} events.")
        print(f"All responses have been saved to data/api_responses/ directories.")
    except Exception as e:
        print(f"❌ Sports data retrieval failed: {e}")

    print("\n✨ Initialization complete!")
    print("The betting bot has successfully connected to your SharpXch account.")
    print("\nNext steps for implementation:")
    print("1. Sports and matches data retrieval")
    print("2. Betting strategy implementation")
    print("3. Automated bet placement")

    return 0


if __name__ == "__main__":
    exit(main())
