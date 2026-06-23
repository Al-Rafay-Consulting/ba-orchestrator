"""
Logging configuration for BA Engine Orchestrator
"""

import logging
import sys
from datetime import datetime

# Create logs directory if it doesn't exist
import os
os.makedirs("logs", exist_ok=True)


def setup_logger(name: str) -> logging.Logger:
    """Configure and return a logger instance"""
    
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    
    # Log format
    log_format = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(log_format)
    logger.addHandler(console_handler)
    
    # File handler
    log_file = f"logs/app_{datetime.now().strftime('%Y%m%d')}.log"
    file_handler = logging.FileHandler(log_file)
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(log_format)
    logger.addHandler(file_handler)
    
    return logger


# Create app logger
logger = setup_logger("BA-Orchestrator")
