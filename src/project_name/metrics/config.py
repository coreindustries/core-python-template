"""Metrics configuration settings.

Settings for Prometheus metrics collection.
"""

from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class MetricsSettings(BaseSettings):
    """Metrics configuration settings.

    Attributes:
        enabled: Enable metrics collection.
        prefix: Prefix for all metric names.
        include_in_schema: Include /metrics in OpenAPI schema.
        default_labels: Default labels to add to all metrics.
    """

    model_config = SettingsConfigDict(
        env_file=".env",
        env_prefix="METRICS_",
        extra="ignore",
    )

    enabled: bool = True
    prefix: str = "project_name"
    include_in_schema: bool = False

    # Histogram buckets for request latency (in seconds)
    histogram_buckets: tuple[float, ...] = Field(
        default=(0.005, 0.01, 0.025, 0.05, 0.1, 0.25, 0.5, 1.0, 2.5, 5.0, 10.0),
    )


@lru_cache
def get_metrics_settings() -> MetricsSettings:
    """Get cached metrics settings instance.

    Returns:
        MetricsSettings singleton instance.
    """
    return MetricsSettings()
