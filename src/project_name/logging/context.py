"""Logging context management.

Provides correlation IDs and request context for distributed tracing.
"""

from contextvars import ContextVar
from dataclasses import dataclass, field
from datetime import UTC, datetime
from typing import Any
from uuid import uuid4


# Context variables for async-safe storage
_correlation_id: ContextVar[str | None] = ContextVar("correlation_id", default=None)
_request_context: ContextVar[dict[str, Any] | None] = ContextVar(
    "request_context", default=None
)


def get_correlation_id() -> str | None:
    """Get the current correlation ID.

    Returns:
        Correlation ID or None if not set.
    """
    return _correlation_id.get()


def set_correlation_id(correlation_id: str | None = None) -> str:
    """Set the correlation ID for the current context.

    Args:
        correlation_id: ID to set, or None to generate a new one.

    Returns:
        The correlation ID that was set.
    """
    cid = correlation_id or str(uuid4())
    _correlation_id.set(cid)
    return cid


def clear_correlation_id() -> None:
    """Clear the correlation ID from the current context."""
    _correlation_id.set(None)


def get_request_context() -> dict[str, Any] | None:
    """Get the current request context.

    Returns:
        Request context dictionary or None if not set.
    """
    return _request_context.get()


def set_request_context(context: dict[str, Any]) -> None:
    """Set the request context for the current async context.

    Args:
        context: Request context dictionary.
    """
    _request_context.set(context)


def clear_request_context() -> None:
    """Clear the request context from the current async context."""
    _request_context.set(None)


@dataclass
class LogContext:
    """Context manager for logging context.

    Automatically manages correlation ID and request context
    for a block of code.

    Example:
        async with LogContext(user_id="123", action="login"):
            logger.info("User action")
    """

    correlation_id: str | None = None
    user_id: str | None = None
    session_id: str | None = None
    ip_address: str | None = None
    user_agent: str | None = None
    method: str | None = None
    path: str | None = None
    extra: dict[str, Any] = field(default_factory=dict)

    _token_cid: Any = field(default=None, repr=False)
    _token_ctx: Any = field(default=None, repr=False)

    def __enter__(self) -> "LogContext":
        """Enter context and set logging context."""
        # Set correlation ID
        self._token_cid = _correlation_id.set(self.correlation_id or str(uuid4()))

        # Build and set request context
        context: dict[str, Any] = {
            "timestamp": datetime.now(UTC).isoformat(),
        }

        if self.user_id:
            context["user_id"] = self.user_id
        if self.session_id:
            context["session_id"] = self.session_id
        if self.ip_address:
            context["ip_address"] = self.ip_address
        if self.user_agent:
            context["user_agent"] = self.user_agent
        if self.method:
            context["method"] = self.method
        if self.path:
            context["path"] = self.path
        if self.extra:
            context.update(self.extra)

        self._token_ctx = _request_context.set(context)

        return self

    def __exit__(self, *args: object) -> None:
        """Exit context and clear logging context."""
        _correlation_id.set(None)
        _request_context.set(None)

    async def __aenter__(self) -> "LogContext":
        """Async enter context."""
        return self.__enter__()

    async def __aexit__(self, *args: object) -> None:
        """Async exit context."""
        self.__exit__(*args)
