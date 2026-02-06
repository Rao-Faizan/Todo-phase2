"""Logging Configuration for MCP Server"""

import logging
import sys
from pathlib import Path
from datetime import datetime
from logging.handlers import RotatingFileHandler
import os


def setup_logging(log_level: str = "INFO", log_file: str = None):
    """
    Setup logging configuration for the MCP server

    Args:
        log_level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        log_file: Optional file path for logging
    """
    # Convert string log level to logging constant
    numeric_level = getattr(logging, log_level.upper(), logging.INFO)

    # Create formatters
    detailed_formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(filename)s:%(lineno)d - %(funcName)s() - %(message)s'
    )

    simple_formatter = logging.Formatter(
        '%(asctime)s - %(levelname)s - %(message)s'
    )

    # Get root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(numeric_level)

    # Clear any existing handlers
    root_logger.handlers.clear()

    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(numeric_level)
    console_handler.setFormatter(simple_formatter)
    root_logger.addHandler(console_handler)

    # File handler (if specified)
    if log_file:
        # Create log directory if it doesn't exist
        log_dir = Path(log_file).parent
        log_dir.mkdir(parents=True, exist_ok=True)

        # Create rotating file handler
        file_handler = RotatingFileHandler(
            log_file,
            maxBytes=10*1024*1024,  # 10MB
            backupCount=5
        )
        file_handler.setLevel(numeric_level)
        file_handler.setFormatter(detailed_formatter)
        root_logger.addHandler(file_handler)

    # Specific loggers for different modules
    mcp_logger = logging.getLogger('mcp')
    mcp_logger.setLevel(numeric_level)

    tool_logger = logging.getLogger('mcp.tools')
    tool_logger.setLevel(numeric_level)

    server_logger = logging.getLogger('mcp.server')
    server_logger.setLevel(numeric_level)

    auth_logger = logging.getLogger('mcp.auth')
    auth_logger.setLevel(numeric_level)


def get_logger(name: str):
    """Get a named logger instance"""
    return logging.getLogger(name)


# Default logging configuration
LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
LOG_FILE = os.getenv('LOG_FILE', 'logs/mcp_server.log')

# Setup default logging
setup_logging(LOG_LEVEL, LOG_FILE)