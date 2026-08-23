import logging
import sys
from logging.handlers import RotatingFileHandler
import os

def setup_logger(name: str, log_file: str = "intellirepo.log", level: int = logging.INFO) -> logging.Logger:
    """
    Creates and configures a robust logger for IntelliRepo components.
    
    Args:
        name: The name of the module/component (e.g., 'ctig_parser', 'planner_agent').
        log_file: Path to the log file.
        level: Logging level (default: INFO).
        
    Returns:
        A configured logging.Logger instance.
    """
    logger = logging.getLogger(name)
    logger.setLevel(level)

    # Prevent adding multiple handlers if the logger already exists
    if logger.hasHandlers():
        return logger

    # 1. Define a consistent, professional format
    # Example: 2026-08-23 20:00:00 - [ctig_parser] - INFO - Started AST parsing...
    formatter = logging.Formatter(
        "%(asctime)s - [%(name)s] - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )

    # 2. Console Handler (Outputs to terminal)
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    # 3. File Handler (Outputs to file, rotates when it hits 5MB, keeps 3 backups)
    # This ensures our background processes don't fill up the user's hard drive
    try:
        file_handler = RotatingFileHandler(
            log_file, maxBytes=5 * 1024 * 1024, backupCount=3
        )
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
    except Exception as e:
        # Fallback if file writing fails (e.g., permissions)
        console_handler.setLevel(logging.DEBUG)
        logger.warning(f"Could not initialize file handler for {log_file}: {e}")

    return logger
