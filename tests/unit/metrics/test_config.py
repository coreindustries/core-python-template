"""Tests for metrics configuration."""

import os
from unittest.mock import patch

from project_name.metrics.config import MetricsSettings


class TestMetricsSettings:
    """Tests for MetricsSettings."""

    def test_default_values(self) -> None:
        """Test default configuration values."""
        settings = MetricsSettings()

        assert settings.enabled is True
        assert settings.prefix == "project_name"
        assert settings.include_in_schema is False
        assert len(settings.histogram_buckets) > 0

    def test_env_override(self) -> None:
        """Test environment variable override."""
        env_vars = {
            "METRICS_ENABLED": "false",
            "METRICS_PREFIX": "my_app",
        }

        with patch.dict(os.environ, env_vars):
            settings = MetricsSettings()
            assert settings.enabled is False
            assert settings.prefix == "my_app"

    def test_histogram_buckets(self) -> None:
        """Test histogram buckets are properly ordered."""
        settings = MetricsSettings()
        buckets = list(settings.histogram_buckets)

        # Should be ascending order
        assert buckets == sorted(buckets)

        # Should cover typical response times
        assert buckets[0] < 0.01  # Sub-10ms
        assert buckets[-1] >= 10.0  # At least 10 seconds
