"""Utility functions and helpers.

This module contains shared utility functions used across the application.
"""

from datetime import UTC, datetime
from typing import Any

# Re-export logging utilities for convenience
from project_name.logging import get_logger


def utc_now() -> datetime:
    """Get current UTC datetime.

    Returns:
        Current datetime in UTC.
    """
    return datetime.now(UTC)


def safe_get(data: dict[str, Any], *keys: str, default: Any = None) -> Any:
    """Safely get nested dictionary value.

    Args:
        data: Dictionary to search.
        keys: Sequence of keys to traverse.
        default: Default value if key not found.

    Returns:
        Value at nested key path or default.

    Example:
        data = {"a": {"b": {"c": 1}}}
        safe_get(data, "a", "b", "c")  # Returns 1
        safe_get(data, "a", "x", "c")  # Returns None
    """
    result: Any = data
    for key in keys:
        if isinstance(result, dict):
            result = result.get(key, default)
        else:
            return default
    return result


__all__ = [
    "get_logger",
    "safe_get",
    "utc_now",
]
