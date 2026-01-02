"""Application logger utilities.

Provides a simple interface for getting configured loggers.
"""

import logging
from typing import Any


def get_logger(name: str) -> logging.Logger:
    """Get a logger with the specified name.

    This is a convenience wrapper around logging.getLogger that
    ensures consistent logger naming and configuration.

    Args:
        name: Logger name (typically __name__).

    Returns:
        Configured logger instance.
    """
    return logging.getLogger(name)


class BoundLogger:
    """Logger with bound context for structured logging.

    Allows binding key-value pairs to a logger that will be
    included in all subsequent log messages.
    """

    def __init__(self, logger: logging.Logger, **context: Any) -> None:
        """Initialize bound logger.

        Args:
            logger: Base logger to wrap.
            **context: Key-value pairs to bind.
        """
        self._logger = logger
        self._context = context

    def bind(self, **context: Any) -> "BoundLogger":
        """Create new bound logger with additional context.

        Args:
            **context: Additional key-value pairs to bind.

        Returns:
            New BoundLogger with merged context.
        """
        return BoundLogger(self._logger, **{**self._context, **context})

    def _log(self, level: int, msg: str, *args: Any, **kwargs: Any) -> None:
        """Internal log method.

        Args:
            level: Logging level.
            msg: Message to log.
            *args: Message arguments.
            **kwargs: Additional keyword arguments.
        """
        extra = kwargs.pop("extra", {})
        extra.update(self._context)
        self._logger.log(level, msg, *args, extra=extra, **kwargs)

    def debug(self, msg: str, *args: Any, **kwargs: Any) -> None:
        """Log debug message."""
        self._log(logging.DEBUG, msg, *args, **kwargs)

    def info(self, msg: str, *args: Any, **kwargs: Any) -> None:
        """Log info message."""
        self._log(logging.INFO, msg, *args, **kwargs)

    def warning(self, msg: str, *args: Any, **kwargs: Any) -> None:
        """Log warning message."""
        self._log(logging.WARNING, msg, *args, **kwargs)

    def error(self, msg: str, *args: Any, **kwargs: Any) -> None:
        """Log error message."""
        self._log(logging.ERROR, msg, *args, **kwargs)

    def critical(self, msg: str, *args: Any, **kwargs: Any) -> None:
        """Log critical message."""
        self._log(logging.CRITICAL, msg, *args, **kwargs)

    def exception(self, msg: str, *args: Any, **kwargs: Any) -> None:
        """Log exception with traceback."""
        kwargs["exc_info"] = True
        self._log(logging.ERROR, msg, *args, **kwargs)


def get_bound_logger(name: str, **context: Any) -> BoundLogger:
    """Get a bound logger with initial context.

    Args:
        name: Logger name (typically __name__).
        **context: Initial context to bind.

    Returns:
        BoundLogger instance.
    """
    return BoundLogger(logging.getLogger(name), **context)
