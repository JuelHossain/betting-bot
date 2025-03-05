"""
Betting strategies configuration.
"""
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Betting limits and thresholds
MAX_STAKE = float(os.getenv('MAX_STAKE', 100))
MIN_ODDS = float(os.getenv('MIN_ODDS', 1.5))
MAX_DAILY_LOSS = float(os.getenv('MAX_DAILY_LOSS', 500))

# Strategy parameters
STRATEGIES = {
    "value_betting": {
        "enabled": True,
        "min_value": 0.05,  # Minimum edge for value bet
        "confidence_threshold": 0.7,  # Minimum confidence
    },
    "arbitrage": {
        "enabled": False,
        "min_profit": 0.02,  # Minimum profit margin
    }
}

# Sport preferences
PREFERRED_SPORTS = ['Soccer', 'Tennis', 'Basketball']

# Markets preferences
PREFERRED_MARKETS = ['Match Result', 'Over/Under', 'Both Teams to Score']
