import logging
import os
import sys
from enum import Enum
from typing import Union

from loguru import logger


class LoggingFormat(str, Enum):
    CONSOLE = "CONSOLE"
    JSON = "JSON"


def analytics_filter(record: dict) -> bool:
    # Keep only events explicitly marked analytics=True in 'extra'
    return record.get("extra", {}).get("analytics", False)


def inv_analytics_filter(record: dict) -> bool:
    # Drop analytics events from normal streams
    return not record.get("extra", {}).get("analytics", False)


def _coerce_level(level: Union[str, int]) -> int:
    if isinstance(level, int):
        return level
    if isinstance(level, str):
        lvl = logging.getLevelName(level.upper())
        return lvl if isinstance(lvl, int) else logging.INFO
    return logging.INFO


def setup_logger(
    level: Union[str, int] = "INFO", fmt: LoggingFormat = LoggingFormat.CONSOLE
):
    """
    Configure loguru logger with either pretty console or JSON output.
    - Non-analytics logs go to stdout by default.
    - Analytics logs (extra={'analytics': True}) go to a JSON sink
      if LOG_DIR is set (file), otherwise they’re suppressed unless JSON mode.
    - If fmt=JSON and LOG_SANE=0 (default), stdout is JSON serialized.
    """
    lvl = _coerce_level(level)

    # Remove default sink(s)
    try:
        logger.remove()  # remove the default handler
    except Exception:
        pass

    log_sane = os.getenv("LOG_SANE", "0").lower()
    log_dir = os.getenv("LOG_DIR", "").strip()

    if fmt == LoggingFormat.JSON and log_sane == "0":
        # JSON to stdout (non-analytics only)
        logger.add(
            sys.stdout,
            level=lvl,
            filter=inv_analytics_filter,
            serialize=True,  # loguru will output structured JSON
            backtrace=False,
            diagnose=False,
        )
    else:
        # Colorized human-readable console (non-analytics only)
        logger.add(
            sys.stdout,
            level=lvl,
            filter=inv_analytics_filter,
            colorize=True,
            format="<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | "
            "<level>{level: <8}</level> | "
            "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - "
            "<level>{message}</level>",
            backtrace=False,
            diagnose=False,
        )

    # Optional analytics file sink (JSON)
    if log_dir:
        os.makedirs(log_dir, exist_ok=True)
        pid = os.getpid()
        log_file = os.path.join(log_dir, f"pr-agent.{pid}.log")
        logger.add(
            log_file,
            level=lvl,
            filter=analytics_filter,  # only analytics events
            serialize=True,  # structured JSON
            rotation="10 MB",
            retention="5 days",
            backtrace=False,
            diagnose=False,
        )

    return logger


def get_logger(*_args, **_kwargs):
    # Provided for backward compatibility with existing imports
    return logger
