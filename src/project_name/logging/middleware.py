"""FastAPI middleware for forensic request/response logging.

Provides comprehensive audit logging for all HTTP requests.
"""

import time
from collections.abc import Callable
from typing import Any

from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.types import ASGIApp

from project_name.logging.audit import AuditAction, AuditLogger, SecurityEvent
from project_name.logging.context import LogContext, set_correlation_id
from project_name.logging.logger import get_logger


logger = get_logger(__name__)


class RequestLoggingMiddleware(BaseHTTPMiddleware):
    """Middleware for logging HTTP requests and responses.

    Captures detailed request/response information for forensic analysis:
    - Request method, path, headers
    - Client IP address and user agent
    - Response status and timing
    - Correlation IDs for distributed tracing
    """

    def __init__(
        self,
        app: ASGIApp,
        *,
        exclude_paths: list[str] | None = None,
        log_request_body: bool = False,
        log_response_body: bool = False,
        max_body_length: int = 1000,
    ) -> None:
        """Initialize middleware.

        Args:
            app: ASGI application.
            exclude_paths: Paths to exclude from logging (e.g., /health).
            log_request_body: Whether to log request bodies.
            log_response_body: Whether to log response bodies.
            max_body_length: Maximum body length to log.
        """
        super().__init__(app)
        self.exclude_paths = exclude_paths or ["/health", "/metrics", "/favicon.ico"]
        self.log_request_body = log_request_body
        self.log_response_body = log_response_body
        self.max_body_length = max_body_length
        self._audit_logger = AuditLogger()

    async def dispatch(
        self, request: Request, call_next: Callable[[Request], Any]
    ) -> Response:
        """Process request and log details.

        Args:
            request: Incoming request.
            call_next: Next middleware/handler.

        Returns:
            Response from the application.
        """
        # Skip excluded paths
        if any(request.url.path.startswith(path) for path in self.exclude_paths):
            return await call_next(request)  # type: ignore[no-any-return]

        # Extract request metadata
        correlation_id = self._get_correlation_id(request)
        client_ip = self._get_client_ip(request)
        user_agent = request.headers.get("user-agent", "")
        user_id = self._get_user_id(request)

        # Set up logging context
        set_correlation_id(correlation_id)

        # Start timing
        start_time = time.perf_counter()

        # Log request
        request_log = {
            "method": request.method,
            "path": request.url.path,
            "query": str(request.query_params) if request.query_params else None,
            "ip_address": client_ip,
            "user_agent": user_agent,
            "user_id": user_id,
            "correlation_id": correlation_id,
            "headers": self._safe_headers(request.headers),
        }

        # Optionally log request body
        if self.log_request_body and request.method in ("POST", "PUT", "PATCH"):
            request_log["body"] = await self._get_request_body(request)

        logger.info(
            "Request started",
            extra={"request": request_log, "event_type": "http_request"},
        )

        # Use logging context for the request
        async with LogContext(
            correlation_id=correlation_id,
            user_id=user_id,
            ip_address=client_ip,
            user_agent=user_agent,
            method=request.method,
            path=request.url.path,
        ):
            try:
                response = await call_next(request)
            except Exception as exc:
                # Log error and re-raise
                duration_ms = (time.perf_counter() - start_time) * 1000
                self._log_error(
                    request, exc, duration_ms, client_ip, user_agent, user_id
                )
                raise

        # Calculate duration
        duration_ms = (time.perf_counter() - start_time) * 1000

        # Log response
        response_log = {
            "method": request.method,
            "path": request.url.path,
            "status_code": response.status_code,
            "duration_ms": round(duration_ms, 2),
            "ip_address": client_ip,
            "user_id": user_id,
            "correlation_id": correlation_id,
        }

        # Determine log level based on status code
        if response.status_code >= 500:
            logger.error(
                "Request completed with server error",
                extra={"response": response_log, "event_type": "http_response"},
            )
        elif response.status_code >= 400:
            logger.warning(
                "Request completed with client error",
                extra={"response": response_log, "event_type": "http_response"},
            )
        else:
            logger.info(
                "Request completed",
                extra={"response": response_log, "event_type": "http_response"},
            )

        # Add correlation ID to response headers
        response.headers["X-Correlation-ID"] = correlation_id

        return response  # type: ignore[no-any-return]

    def _get_correlation_id(self, request: Request) -> str:
        """Get or generate correlation ID.

        Args:
            request: Incoming request.

        Returns:
            Correlation ID string.
        """
        # Check for existing correlation ID in headers
        correlation_id = request.headers.get("X-Correlation-ID")
        if correlation_id:
            return correlation_id

        correlation_id = request.headers.get("X-Request-ID")
        if correlation_id:
            return correlation_id

        # Generate new ID
        import uuid

        return str(uuid.uuid4())

    def _get_client_ip(self, request: Request) -> str:
        """Extract client IP address.

        Handles proxied requests by checking forwarded headers.

        Args:
            request: Incoming request.

        Returns:
            Client IP address.
        """
        # Check forwarded headers (in order of preference)
        forwarded_for = request.headers.get("X-Forwarded-For")
        if forwarded_for:
            # X-Forwarded-For can contain multiple IPs; take the first (client)
            return forwarded_for.split(",")[0].strip()

        real_ip = request.headers.get("X-Real-IP")
        if real_ip:
            return real_ip

        # Fall back to direct client
        if request.client:
            return request.client.host

        return "unknown"

    def _get_user_id(self, request: Request) -> str | None:
        """Extract user ID from request.

        Override this method to integrate with your authentication system.

        Args:
            request: Incoming request.

        Returns:
            User ID or None if not authenticated.
        """
        # Check for user in request state (set by auth middleware)
        if hasattr(request.state, "user") and request.state.user:
            return getattr(request.state.user, "id", None)

        # Check for user ID in headers (e.g., from API gateway)
        return request.headers.get("X-User-ID")

    def _safe_headers(self, headers: Any) -> dict[str, str]:
        """Extract headers, excluding sensitive ones.

        Args:
            headers: Request headers.

        Returns:
            Dictionary of safe headers.
        """
        sensitive_headers = {
            "authorization",
            "cookie",
            "x-api-key",
            "x-auth-token",
            "x-csrf-token",
        }

        return {
            k: v if k.lower() not in sensitive_headers else "[REDACTED]"
            for k, v in headers.items()
        }

    async def _get_request_body(self, request: Request) -> str | None:
        """Get request body for logging.

        Args:
            request: Incoming request.

        Returns:
            Request body string or None.
        """
        try:
            body = await request.body()
            if body:
                body_str = body.decode("utf-8", errors="replace")
                if len(body_str) > self.max_body_length:
                    return body_str[: self.max_body_length] + "...[truncated]"
                return body_str
        except Exception:  # noqa: S110  # nosec B110  # Ignore decode errors silently
            pass
        return None

    def _log_error(
        self,
        request: Request,
        exc: Exception,
        duration_ms: float,
        client_ip: str,
        user_agent: str,
        user_id: str | None,
    ) -> None:
        """Log request error.

        Args:
            request: Request that caused the error.
            exc: Exception that was raised.
            duration_ms: Request duration in milliseconds.
            client_ip: Client IP address.
            user_agent: Client user agent.
            user_id: User ID if available.
        """
        logger.exception(
            "Request failed with exception",
            extra={
                "event_type": "http_error",
                "error": {
                    "type": type(exc).__name__,
                    "message": str(exc),
                },
                "request": {
                    "method": request.method,
                    "path": request.url.path,
                    "ip_address": client_ip,
                    "user_agent": user_agent,
                    "user_id": user_id,
                    "duration_ms": round(duration_ms, 2),
                },
            },
        )

        # Log security event for errors
        self._audit_logger.log_event(
            SecurityEvent(
                action=AuditAction.API_ERROR,
                actor_id=user_id,
                ip_address=client_ip,
                user_agent=user_agent,
                details=f"Request error: {type(exc).__name__}: {exc}",
                metadata={
                    "method": request.method,
                    "path": request.url.path,
                    "error_type": type(exc).__name__,
                },
            )
        )
