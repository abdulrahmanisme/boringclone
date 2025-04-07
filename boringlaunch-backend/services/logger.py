import sys
from pathlib import Path
from loguru import logger
from datetime import datetime

# Create logs directory if it doesn't exist
LOGS_DIR = Path("logs")
LOGS_DIR.mkdir(exist_ok=True)

# Configure loguru logger
logger.remove()  # Remove default handler

# Add console handler for development
logger.add(
    sys.stdout,
    format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>",
    level="DEBUG" if __debug__ else "INFO",
    diagnose=True,
)

# Add file handler for errors
logger.add(
    LOGS_DIR / "error_{time:YYYY-MM-DD}.log",
    format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function}:{line} - {message}",
    level="ERROR",
    rotation="00:00",  # Create new file at midnight
    retention="30 days",  # Keep logs for 30 days
    compression="zip",
    diagnose=True,
)

# Add file handler for all logs
logger.add(
    LOGS_DIR / "app_{time:YYYY-MM-DD}.log",
    format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function}:{line} - {message}",
    level="INFO",
    rotation="00:00",
    retention="7 days",
    compression="zip",
)

class Logger:
    @staticmethod
    def debug(message: str, *args, **kwargs):
        logger.debug(message, *args, **kwargs)

    @staticmethod
    def info(message: str, *args, **kwargs):
        logger.info(message, *args, **kwargs)

    @staticmethod
    def warning(message: str, *args, **kwargs):
        logger.warning(message, *args, **kwargs)

    @staticmethod
    def error(message: str, *args, **kwargs):
        logger.error(message, *args, **kwargs)

    @staticmethod
    def exception(message: str, *args, **kwargs):
        logger.exception(message, *args, **kwargs)

    @staticmethod
    def critical(message: str, *args, **kwargs):
        logger.critical(message, *args, **kwargs)

# Create global logger instance
log = Logger() 