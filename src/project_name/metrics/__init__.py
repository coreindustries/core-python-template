"""Prometheus metrics module.

HTTP and AI metrics collection with Prometheus.

Example:
    >>> from project_name.metrics import get_metrics_collector
    >>>
    >>> collector = get_metrics_collector()
    >>> collector.record_request("GET", "/api/users", "200", 0.05)
"""

from project_name.metrics.collector import (
    MetricsCollector,
    get_metrics_collector,
)
from project_name.metrics.config import (
    MetricsSettings,
    get_metrics_settings,
)
from project_name.metrics.middleware import PrometheusMetricsMiddleware


__all__ = [
    "MetricsCollector",
    "MetricsSettings",
    "PrometheusMetricsMiddleware",
    "get_metrics_collector",
    "get_metrics_settings",
]
