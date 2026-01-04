"""Prometheus metrics collector.

Centralized metrics definitions following Prometheus conventions.
"""

from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from prometheus_client import Counter, Gauge, Histogram, Info


class MetricsCollector:
    """Centralized metrics collector.

    Provides HTTP and AI-related metrics following Prometheus naming conventions.

    Attributes:
        request_count: Total HTTP requests counter.
        request_latency: Request latency histogram.
        requests_in_progress: Current in-progress requests gauge.
        app_info: Application information gauge.
        ai_token_usage: AI token consumption counter.
        ai_request_latency: AI request latency histogram.
    """

    def __init__(self, prefix: str = "project_name") -> None:
        """Initialize metrics collector.

        Args:
            prefix: Prefix for all metric names.
        """
        self._prefix = prefix
        self._initialized = False

        # Lazy initialization - metrics created on first use
        self._request_count: Counter | None = None
        self._request_latency: Histogram | None = None
        self._requests_in_progress: Gauge | None = None
        self._app_info: Info | None = None
        self._ai_token_usage: Counter | None = None
        self._ai_request_latency: Histogram | None = None

    def _initialize(self) -> None:
        """Initialize Prometheus metrics."""
        if self._initialized:
            return

        try:
            from prometheus_client import (  # noqa: PLC0415
                Counter,
                Gauge,
                Histogram,
                Info,
            )
        except ImportError as e:
            raise ImportError(
                "prometheus-client not installed. "
                "Install with: uv add prometheus-client"
            ) from e

        # HTTP metrics
        self._request_count = Counter(
            f"{self._prefix}_http_requests_total",
            "Total HTTP requests",
            ["method", "endpoint", "status"],
        )

        self._request_latency = Histogram(
            f"{self._prefix}_http_request_duration_seconds",
            "HTTP request latency in seconds",
            ["method", "endpoint"],
            buckets=(0.005, 0.01, 0.025, 0.05, 0.1, 0.25, 0.5, 1.0, 2.5, 5.0, 10.0),
        )

        self._requests_in_progress = Gauge(
            f"{self._prefix}_http_requests_in_progress",
            "HTTP requests currently in progress",
            ["method", "endpoint"],
        )

        self._app_info = Info(
            f"{self._prefix}_app",
            "Application information",
        )

        # AI metrics
        self._ai_token_usage = Counter(
            f"{self._prefix}_ai_tokens_total",
            "Total AI tokens consumed",
            ["model", "token_type"],  # token_type: prompt or completion
        )

        self._ai_request_latency = Histogram(
            f"{self._prefix}_ai_request_duration_seconds",
            "AI request latency in seconds",
            ["provider", "model", "operation"],  # operation: chat, embed
            buckets=(0.1, 0.25, 0.5, 1.0, 2.5, 5.0, 10.0, 30.0, 60.0),
        )

        self._initialized = True

    @property
    def request_count(self) -> "Counter":
        """Get HTTP request counter.

        Returns:
            Prometheus Counter for request counts.
        """
        self._initialize()
        assert self._request_count is not None  # nosec B101  # Type narrowing after init
        return self._request_count

    @property
    def request_latency(self) -> "Histogram":
        """Get HTTP request latency histogram.

        Returns:
            Prometheus Histogram for request latency.
        """
        self._initialize()
        assert self._request_latency is not None  # nosec B101  # Type narrowing after init
        return self._request_latency

    @property
    def requests_in_progress(self) -> "Gauge":
        """Get in-progress requests gauge.

        Returns:
            Prometheus Gauge for in-progress requests.
        """
        self._initialize()
        assert self._requests_in_progress is not None  # nosec B101  # Type narrowing after init
        return self._requests_in_progress

    @property
    def app_info(self) -> "Info":
        """Get application info metric.

        Returns:
            Prometheus Info for application metadata.
        """
        self._initialize()
        assert self._app_info is not None  # nosec B101  # Type narrowing after init
        return self._app_info

    @property
    def ai_token_usage(self) -> "Counter":
        """Get AI token usage counter.

        Returns:
            Prometheus Counter for AI token usage.
        """
        self._initialize()
        assert self._ai_token_usage is not None  # nosec B101  # Type narrowing after init
        return self._ai_token_usage

    @property
    def ai_request_latency(self) -> "Histogram":
        """Get AI request latency histogram.

        Returns:
            Prometheus Histogram for AI request latency.
        """
        self._initialize()
        assert self._ai_request_latency is not None  # nosec B101  # Type narrowing after init
        return self._ai_request_latency

    def set_app_info(self, version: str, environment: str) -> None:
        """Set application info metric.

        Args:
            version: Application version.
            environment: Deployment environment.
        """
        self.app_info.info(
            {
                "version": version,
                "environment": environment,
            }
        )

    def record_request(
        self,
        method: str,
        endpoint: str,
        status: str,
        duration: float,
    ) -> None:
        """Record an HTTP request.

        Args:
            method: HTTP method.
            endpoint: Request endpoint (normalized).
            status: HTTP status code as string.
            duration: Request duration in seconds.
        """
        self.request_count.labels(
            method=method,
            endpoint=endpoint,
            status=status,
        ).inc()

        self.request_latency.labels(
            method=method,
            endpoint=endpoint,
        ).observe(duration)

    def record_ai_request(
        self,
        provider: str,
        model: str,
        operation: str,
        duration: float,
        prompt_tokens: int = 0,
        completion_tokens: int = 0,
    ) -> None:
        """Record an AI request.

        Args:
            provider: AI provider name.
            model: Model used.
            operation: Operation type (chat, embed).
            duration: Request duration in seconds.
            prompt_tokens: Input tokens.
            completion_tokens: Output tokens.
        """
        self.ai_request_latency.labels(
            provider=provider,
            model=model,
            operation=operation,
        ).observe(duration)

        if prompt_tokens > 0:
            self.ai_token_usage.labels(
                model=model,
                token_type="prompt",  # nosec B106  # Not a password, token type label
            ).inc(prompt_tokens)

        if completion_tokens > 0:
            self.ai_token_usage.labels(
                model=model,
                token_type="completion",  # nosec B106  # Not a password, token type label
            ).inc(completion_tokens)


# Global collector instance
_collector: MetricsCollector | None = None


def get_metrics_collector() -> MetricsCollector:
    """Get the global metrics collector instance.

    Returns:
        MetricsCollector singleton instance.
    """
    global _collector  # noqa: PLW0603
    if _collector is None:
        from project_name.metrics.config import get_metrics_settings  # noqa: PLC0415

        settings = get_metrics_settings()
        _collector = MetricsCollector(prefix=settings.prefix)
    return _collector
