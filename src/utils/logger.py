"""
Logger configuration module for the betting bot application.
"""
import sys
from pathlib import Path
from loguru import logger

from .config import LOG_LEVEL, LOG_FILE, ROOT_DIR

# Configure loguru logger
def configure_logger():
    """Configure the logger for the application."""
    # Remove default logger
    logger.remove()
    
    # Add console logger
    logger.add(
        sys.stdout,
        format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>",
        level=LOG_LEVEL,
    )
    
    # Add file logger
    log_file_path = ROOT_DIR / LOG_FILE
    logger.add(
        log_file_path,
        format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function}:{line} - {message}",
        level=LOG_LEVEL,
        rotation="10 MB",
        retention="7 days",
    )
    
    return logger

# Create and configure logger instance
logger = configure_logger()
