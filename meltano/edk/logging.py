"""Recommended logging configuration for extensions."""

from __future__ import annotations

import logging
import os
import sys
from typing import Callable

import structlog

LEVELS = {  # noqa: WPS407
    "debug": logging.DEBUG,
    "info": logging.INFO,
    "warning": logging.WARNING,
    "error": logging.ERROR,
    "critical": logging.CRITICAL,
}

DEFAULT_LEVEL = "info"


def strtobool(val: str) -> bool:
    """Convert a string representation of truth to true (1) or false (0).

    True values are 'y', 'yes', 't', 'true', 'on', and '1'; false values
    are 'n', 'no', 'f', 'false', 'off', and '0'.  Raises ValueError if
    'val' is anything else.

    Case is ignored in string comparisons.

    Re-implemented from distutils.util.strtobool to avoid importing distutils.

    Args:
        val: The string to convert to a boolean.

    Returns:
        True if the string represents a truthy value, False otherwise.

    Raises:
        ValueError: If the string is not a valid representation of a boolean.
    """
    val = val.lower()
    if val in {"y", "yes", "t", "true", "on", "1"}:
        return True
    elif val in {"n", "no", "f", "false", "off", "0"}:
        return False

    raise ValueError(f"invalid truth value {val!r}")


def parse_log_level(log_level: str) -> int:
    """Parse a level descriptor into an logging level.

    Args:
        log_level: level descriptor.

    Returns:
        int: actual logging level.
    """
    return LEVELS.get(log_level.lower(), LEVELS[DEFAULT_LEVEL])


def default_logging_config(
    level: int = logging.INFO,
    timestamps: bool = False,
    levels: bool = False,
    json_format: bool = False,
) -> None:
    """default/demo structlog configuration.

    Args:
        level: logging level.
        timestamps: include timestamps in the log.
        levels: include levels in the log.
        json_format: if True, use JSON format, otherwise use human-readable format.
    """
    processors: list[Callable] = []
    if timestamps:
        processors.append(structlog.processors.TimeStamper(fmt="iso"))
    if levels:
        processors.append(structlog.processors.add_log_level)

    renderer: structlog.processors.JSONRenderer | structlog.dev.ConsoleRenderer = (
        structlog.processors.JSONRenderer()
        if json_format
        else structlog.dev.ConsoleRenderer(colors=False)
    )

    processors.extend(
        [
            # If log level is too low, abort pipeline and throw away log entry.
            structlog.stdlib.filter_by_level,
            # If the "stack_info" key in the event dict is true, remove it and
            # render the current stack trace in the "stack" key.
            structlog.processors.StackInfoRenderer(),
            # If the "exc_info" key in the event dict is either true or a
            # sys.exc_info() tuple, remove "exc_info" and render the exception
            # with traceback into the "exception" key.
            structlog.processors.format_exc_info,
            # If some value is in bytes, decode it to a unicode str.
            structlog.processors.UnicodeDecoder(),
            structlog.processors.ExceptionPrettyPrinter(),
            # Render the final event dict as JSON.
            renderer,
        ]
    )

    structlog.configure(
        processors=processors,
        # `wrapper_class` is the bound logger that you get back from
        # get_logger(). This one imitates the API of `logging.Logger`.
        wrapper_class=structlog.stdlib.BoundLogger,
        # `logger_factory` is used to create wrapped loggers that are used for
        # OUTPUT. This one returns a `logging.Logger`. The final value (a JSON
        # string) from the final processor (`JSONRenderer`) will be passed to
        # the method of the same name as that you've called on the bound logger.
        logger_factory=structlog.stdlib.LoggerFactory(),
        # Effectively freeze configuration after creating the first bound
        # logger.
        cache_logger_on_first_use=True,
    )

    logging.basicConfig(
        format="%(message)s",
        stream=sys.stderr,
        level=level,
    )


def pass_through_logging_config() -> None:
    """Pass-through logging configuration.

    Setups a logging config using the LOG_LEVEL, LOG_TIMESTAMPS, LOG_LEVELS,
    and MELTANO_LOG_JSON env vars.
    """
    log_level = os.environ.get("LOG_LEVEL", "INFO")
    log_timestamps = os.environ.get("LOG_TIMESTAMPS", "False")
    log_levels = os.environ.get("LOG_LEVELS", "False")
    meltano_log_json = os.environ.get("MELTANO_LOG_JSON", "False")

    default_logging_config(
        level=parse_log_level(log_level),
        timestamps=strtobool(log_timestamps),
        levels=strtobool(log_levels),
        json_format=strtobool(meltano_log_json),
    )
