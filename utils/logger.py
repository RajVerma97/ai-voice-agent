"""
Centralized logging configuration using Loguru.
"""

import sys
import os
from pathlib import Path
from loguru import logger

# Remove default logger
logger.remove()

# Create logs directory
logs_dir = Path(__file__).parent.parent.parent / "logs"
logs_dir.mkdir(exist_ok=True)

# Get log level from environment variable (default to INFO for production)
# Get environment (default to development)
ENV = os.getenv("ENVIRONMENT", "development").lower()

# Environment-specific configurations
ENV_CONFIG = {
    "development": {
        "console_level": "DEBUG",
        "console_format": "<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>",
        "file_level": "DEBUG",
        "file_rotation": "10 MB",
        "file_retention": "7 days",
    },
    "production": {
        "console_level": "INFO",
        "console_format": "{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {message}",
        "file_level": "INFO",
        "file_rotation": "50 MB",
        "file_retention": "30 days",
    },
    "staging": {
        "console_level": "WARNING",
        "console_format": "{level: <8} | {message}",
        "file_level": "DEBUG",
        "file_rotation": "5 MB",
        "file_retention": "3 days",
    },
}

config = ENV_CONFIG.get(ENV, ENV_CONFIG["development"])
console_level = os.getenv("LOG_LEVEL", config["console_level"]).upper()

# Console logger with color
logger.add(
    sys.stderr,
    format=config["console_format"],
    level=console_level,
    colorize=True if ENV == "development" else False,
)

# File logger - general log
logger.add(
    logs_dir / f"app_{ENV}.log",
    rotation=config["file_rotation"],
    retention=config["file_retention"],
    compression="zip",
    format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function}:{line} - {message}",
    level=config["file_level"],
    enqueue=True,  # Async writing for better performance
)
# File logger - error log
logger.add(
    logs_dir / f"error_{ENV}.log",
    rotation="10 MB",
    retention="90 days",
    compression="zip",
    format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function}:{line} - {message}\n{extra}",
    level="ERROR",
    enqueue=True,
    backtrace=True,  # Include full traceback
    diagnose=True if ENV != "production" else False,  # Detailed diagnosis in non-prod
)

logger.info(f"Logger initialized for environment: {ENV}")
logger.debug(f"Console log level: {console_level}")
logger.debug(f"Logs directory: {logs_dir}")

__all__ = ["logger"]
