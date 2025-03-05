"""
Logging configuration for the SharpXch betting bot.
"""
import os
import logging
from pathlib import Path
from datetime import datetime

# Base logging directory
LOG_DIR = os.path.join(Path(__file__).parent.parent, "logs")
os.makedirs(LOG_DIR, exist_ok=True)


def setup_logging(log_level=logging.INFO):
    """
    Set up logging configuration.
    
    Args:
        log_level: The logging level to use
        
    Returns:
        logging.Logger: Configured logger
    """
    # Create a custom logger
    logger = logging.getLogger("betting_bot")
    logger.setLevel(log_level)
    
    # Create handlers
    console_handler = logging.StreamHandler()
    file_handler = logging.FileHandler(
        os.path.join(LOG_DIR, f"betting_bot_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log")
    )
    
    # Create formatters and add to handlers
    log_format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    formatter = logging.Formatter(log_format)
    
    console_handler.setFormatter(formatter)
    file_handler.setFormatter(formatter)
    
    # Add handlers to the logger
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)
    
    return logger
