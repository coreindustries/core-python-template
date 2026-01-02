"""Tests for Prometheus metrics collector."""

from unittest.mock import MagicMock, patch

import pytest

from project_name.metrics.collector import (
    MetricsCollector,
    get_metrics_collector,
)


class TestMetricsCollector:
    """Tests for MetricsCollector class."""

    def test_init_with_default_prefix(self) -> None:
        """Test initialization with default prefix."""
        collector = MetricsCollector()
        assert collector._prefix == "project_name"
        assert collector._initialized is False

    def test_init_with_custom_prefix(self) -> None:
        """Test initialization with custom prefix."""
        collector = MetricsCollector(prefix="my_app")
        assert collector._prefix == "my_app"

    def test_initialize_creates_metrics(self) -> None:
        """Test that _initialize creates all metrics."""
        with patch("prometheus_client.Counter") as mock_counter, patch(
            "prometheus_client.Histogram"
        ) as mock_histogram, patch(
            "prometheus_client.Gauge"
        ) as mock_gauge, patch(
            "prometheus_client.Info"
        ) as mock_info:
            collector = MetricsCollector(prefix="test")
            # Reset initialization state to allow re-init
            collector._initialized = False

            # Access a property to trigger initialization
            _ = collector.request_count

            assert mock_counter.call_count == 2  # request_count, ai_token_usage
            assert mock_histogram.call_count == 2  # request_latency, ai_request_latency
            assert mock_gauge.call_count == 1  # requests_in_progress
            assert mock_info.call_count == 1  # app_info

    def test_initialize_only_once(self) -> None:
        """Test that _initialize only runs once."""
        with patch("prometheus_client.Counter") as mock_counter, patch(
            "prometheus_client.Histogram"
        ), patch("prometheus_client.Gauge"), patch("prometheus_client.Info"):
            collector = MetricsCollector()
            # Reset initialization state
            collector._initialized = False

            # Access properties multiple times
            _ = collector.request_count
            _ = collector.request_latency
            _ = collector.request_count

            # Should only initialize once
            assert collector._initialized is True
            assert mock_counter.call_count == 2

    def test_import_error(self) -> None:
        """Test that ImportError is raised when prometheus-client not installed."""
        with patch.dict("sys.modules", {"prometheus_client": None}):
            collector = MetricsCollector()
            collector._initialized = False

            with pytest.raises(ImportError, match="prometheus-client not installed"):
                collector._initialize()


class TestMetricsCollectorProperties:
    """Tests for MetricsCollector property accessors."""

    def test_request_count(self) -> None:
        """Test request_count property."""
        collector = MetricsCollector()
        # Manually set up the mock metrics
        collector._initialized = True
        collector._request_count = MagicMock()
        assert collector.request_count is not None

    def test_request_latency(self) -> None:
        """Test request_latency property."""
        collector = MetricsCollector()
        collector._initialized = True
        collector._request_latency = MagicMock()
        assert collector.request_latency is not None

    def test_requests_in_progress(self) -> None:
        """Test requests_in_progress property."""
        collector = MetricsCollector()
        collector._initialized = True
        collector._requests_in_progress = MagicMock()
        assert collector.requests_in_progress is not None

    def test_app_info(self) -> None:
        """Test app_info property."""
        collector = MetricsCollector()
        collector._initialized = True
        collector._app_info = MagicMock()
        assert collector.app_info is not None

    def test_ai_token_usage(self) -> None:
        """Test ai_token_usage property."""
        collector = MetricsCollector()
        collector._initialized = True
        collector._ai_token_usage = MagicMock()
        assert collector.ai_token_usage is not None

    def test_ai_request_latency(self) -> None:
        """Test ai_request_latency property."""
        collector = MetricsCollector()
        collector._initialized = True
        collector._ai_request_latency = MagicMock()
        assert collector.ai_request_latency is not None


class TestMetricsCollectorMethods:
    """Tests for MetricsCollector methods."""

    @pytest.fixture
    def collector(self) -> MetricsCollector:
        """Create a collector with mocked metrics."""
        collector = MetricsCollector()
        collector._initialized = True
        collector._request_count = MagicMock()
        collector._request_latency = MagicMock()
        collector._requests_in_progress = MagicMock()
        collector._app_info = MagicMock()
        collector._ai_token_usage = MagicMock()
        collector._ai_request_latency = MagicMock()
        return collector

    def test_set_app_info(self, collector: MetricsCollector) -> None:
        """Test set_app_info method."""
        collector.set_app_info(version="1.0.0", environment="production")

        collector._app_info.info.assert_called_once_with(
            {"version": "1.0.0", "environment": "production"}
        )

    def test_record_request(self, collector: MetricsCollector) -> None:
        """Test record_request method."""
        collector.record_request(
            method="GET",
            endpoint="/api/users",
            status="200",
            duration=0.5,
        )

        collector._request_count.labels.assert_called_with(
            method="GET", endpoint="/api/users", status="200"
        )
        collector._request_latency.labels.assert_called_with(
            method="GET", endpoint="/api/users"
        )

    def test_record_ai_request(self, collector: MetricsCollector) -> None:
        """Test record_ai_request method."""
        collector.record_ai_request(
            provider="openai",
            model="gpt-4o-mini",
            operation="chat",
            duration=1.5,
            prompt_tokens=100,
            completion_tokens=50,
        )

        collector._ai_request_latency.labels.assert_called_with(
            provider="openai", model="gpt-4o-mini", operation="chat"
        )

    def test_record_ai_request_no_tokens(self, collector: MetricsCollector) -> None:
        """Test record_ai_request with zero tokens."""
        collector.record_ai_request(
            provider="openai",
            model="gpt-4o-mini",
            operation="chat",
            duration=1.5,
            prompt_tokens=0,
            completion_tokens=0,
        )

        # Token usage should not be recorded for zero tokens
        # But latency should still be recorded
        collector._ai_request_latency.labels.assert_called_once()


class TestGetMetricsCollector:
    """Tests for get_metrics_collector function."""

    def test_returns_singleton(self) -> None:
        """Test that function returns singleton."""
        import project_name.metrics.collector as collector_module  # noqa: PLC0415

        # Reset global
        collector_module._collector = None

        with patch(
            "project_name.metrics.config.get_metrics_settings"
        ) as mock_settings:
            mock_settings.return_value = MagicMock(prefix="test")

            collector1 = get_metrics_collector()
            collector2 = get_metrics_collector()

            assert collector1 is collector2

        # Clean up
        collector_module._collector = None
