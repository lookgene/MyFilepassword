"""Logging configuration."""

import sys
from typing import Any

from loguru import logger as _logger

from app.core.config import get_settings

settings = get_settings()


def setup_logger() -> Any:
    """Setup loguru logger."""
    # Remove default handler
    _logger.remove()

    # Console handler
    if settings.log_format == "json":
        _logger.add(
            sys.stdout,
            format=(
                '{"time":"{time:YYYY-MM-DD HH:mm:ss.SSS}",'
                '"level":"{level}",'
                '"message":"{message}",'
                '"function":"{function}",'
                '"line":"{line}",'
                '"extra":{"context":"{extra[context]}"}'
                "}"
            ),
            level=settings.log_level,
            enqueue=True,
        )
    else:
        _logger.add(
            sys.stdout,
            format="<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | "
            "<level>{level: <8}</level> | "
            "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> | "
            "<level>{message}</level>",
            level=settings.log_level,
            enqueue=True,
        )

    # File handler for errors
    _logger.add(
        "logs/error.log",
        rotation="1 day",
        retention="30 days",
        level="ERROR",
        format="{time:YYYY-MM-DD HH:mm:ss.SSS} | {level: <8} | {name}:{function}:{line} | {message}",
        enqueue=True,
    )

    # File handler for all logs
    _logger.add(
        "logs/app.log",
        rotation="1 day",
        retention="7 days",
        level=settings.log_level,
        format="{time:YYYY-MM-DD HH:mm:ss.SSS} | {level: <8} | {name}:{function}:{line} | {message}",
        enqueue=True,
    )

    return _logger


logger = setup_logger()
