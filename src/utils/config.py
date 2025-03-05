"""
Configuration module to load and manage environment variables.
"""
import os
from pathlib import Path
from dotenv import load_dotenv

# Find the root directory of the project
ROOT_DIR = Path(__file__).parent.parent.parent

# Load environment variables from .env file
load_dotenv(ROOT_DIR / '.env')

# API Configuration
API_BASE_URL = os.getenv('API_BASE_URL', 'https://afde-apim-alpha-backoffice-prod-westeurope-bvc2d9ccamfjhkhg.z03.azurefd.net')
AUTH_ENDPOINT = os.getenv('AUTH_ENDPOINT', '/backoffice/connect/token')
API_USERNAME = os.getenv('API_USERNAME')
API_PASSWORD = os.getenv('API_PASSWORD')

# Logging Configuration
LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
LOG_FILE = os.getenv('LOG_FILE', 'logs/betting_bot.log')

# Betting Configuration
MAX_STAKE = float(os.getenv('MAX_STAKE', 100))
MIN_ODDS = float(os.getenv('MIN_ODDS', 1.5))
MAX_DAILY_LOSS = float(os.getenv('MAX_DAILY_LOSS', 500))

# Ensure the logs directory exists
def ensure_dirs_exist():
    """Ensure that necessary directories exist."""
    log_dir = Path(LOG_FILE).parent
    if not (ROOT_DIR / log_dir).exists():
        (ROOT_DIR / log_dir).mkdir(parents=True, exist_ok=True)

# Call this function to ensure directories exist when module is imported
ensure_dirs_exist()
