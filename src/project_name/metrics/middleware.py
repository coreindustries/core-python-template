"""Prometheus metrics middleware.

FastAPI middleware for collecting HTTP request metrics.
"""

import re
import time
from collections.abc import Awaitable, Callable

from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.types import ASGIApp

from project_name.metrics.collector import MetricsCollector, get_metrics_collector


# Patterns for normalizing paths
UUID_PATTERN = re.compile(
    r"/[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12}"
)
CUID_PATTERN = re.compile(r"/c[a-z0-9]{24,}")
NUMERIC_ID_PATTERN = re.compile(r"/\d+")


class PrometheusMetricsMiddleware(BaseHTTPMiddleware):
    """Middleware for collecting Prometheus metrics.

    Collects request count, latency, and in-progress metrics
    for all HTTP requests.

    Example:
        >>> app.add_middleware(
        ...     PrometheusMetricsMiddleware,
        ...     exclude_paths=["/health", "/metrics"],
        ... )
    """

    def __init__(
        self,
        app: ASGIApp,
        *,
        collector: MetricsCollector | None = None,
        exclude_paths: list[str] | None = None,
    ) -> None:
        """Initialize metrics middleware.

        Args:
            app: ASGI application.
            collector: Metrics collector instance.
            exclude_paths: Paths to exclude from metrics collection.
        """
        super().__init__(app)
        self._collector = collector or get_metrics_collector()
        self._exclude_paths = exclude_paths or ["/health", "/metrics"]

    async def dispatch(
        self,
        request: Request,
        call_next: Callable[[Request], Awaitable[Response]],
    ) -> Response:
        """Collect metrics for each request.

        Args:
            request: Incoming HTTP request.
            call_next: Next middleware or route handler.

        Returns:
            HTTP response.
        """
        # Skip excluded paths
        path = request.url.path
        if any(path.startswith(excluded) for excluded in self._exclude_paths):
            return await call_next(request)

        method = request.method
        endpoint = self._normalize_path(path)

        # Track in-progress requests
        self._collector.requests_in_progress.labels(
            method=method,
            endpoint=endpoint,
        ).inc()

        # Start timing
        start_time = time.perf_counter()
        status_code = "500"

        try:
            response = await call_next(request)
            status_code = str(response.status_code)
            return response

        except Exception:
            # Re-raise after recording metrics
            raise

        finally:
            # Record metrics
            duration = time.perf_counter() - start_time

            self._collector.record_request(
                method=method,
                endpoint=endpoint,
                status=status_code,
                duration=duration,
            )

            self._collector.requests_in_progress.labels(
                method=method,
                endpoint=endpoint,
            ).dec()

    def _normalize_path(self, path: str) -> str:
        """Normalize path for metric labels.

        Replaces dynamic path segments (IDs) with placeholders
        to prevent high cardinality labels.

        Args:
            path: Request path.

        Returns:
            Normalized path with ID placeholders.
        """
        # Replace UUIDs
        path = UUID_PATTERN.sub("/{id}", path)
        # Replace CUIDs
        path = CUID_PATTERN.sub("/{id}", path)
        # Replace numeric IDs
        path = NUMERIC_ID_PATTERN.sub("/{id}", path)

        return path
