"""Tests for metrics middleware."""

from project_name.metrics.middleware import (
    CUID_PATTERN,
    NUMERIC_ID_PATTERN,
    UUID_PATTERN,
    PrometheusMetricsMiddleware,
)


class TestPathNormalization:
    """Tests for path normalization patterns."""

    def test_uuid_pattern(self) -> None:
        """Test UUID pattern matching."""
        path = "/users/123e4567-e89b-12d3-a456-426614174000/profile"
        result = UUID_PATTERN.sub("/{id}", path)
        assert result == "/users/{id}/profile"

    def test_cuid_pattern(self) -> None:
        """Test CUID pattern matching."""
        path = "/users/clrk0q1234567890abcdef123456/profile"
        result = CUID_PATTERN.sub("/{id}", path)
        assert result == "/users/{id}/profile"

    def test_numeric_id_pattern(self) -> None:
        """Test numeric ID pattern matching."""
        path = "/users/12345/posts/67890"
        result = NUMERIC_ID_PATTERN.sub("/{id}", path)
        assert result == "/users/{id}/posts/{id}"

    def test_no_match(self) -> None:
        """Test path without IDs."""
        path = "/health"
        result = UUID_PATTERN.sub("/{id}", path)
        result = NUMERIC_ID_PATTERN.sub("/{id}", result)
        assert result == "/health"


class TestPrometheusMetricsMiddleware:
    """Tests for PrometheusMetricsMiddleware."""

    def test_normalize_path_uuid(self) -> None:
        """Test path normalization with UUID."""
        # Create middleware without app (just for testing method)
        middleware = PrometheusMetricsMiddleware(app=None)  # type: ignore[arg-type]

        path = "/api/users/550e8400-e29b-41d4-a716-446655440000"
        normalized = middleware._normalize_path(path)
        assert normalized == "/api/users/{id}"

    def test_normalize_path_numeric(self) -> None:
        """Test path normalization with numeric ID."""
        middleware = PrometheusMetricsMiddleware(app=None)  # type: ignore[arg-type]

        path = "/api/posts/12345/comments/67890"
        normalized = middleware._normalize_path(path)
        assert normalized == "/api/posts/{id}/comments/{id}"

    def test_normalize_path_no_ids(self) -> None:
        """Test path normalization without IDs."""
        middleware = PrometheusMetricsMiddleware(app=None)  # type: ignore[arg-type]

        path = "/api/health"
        normalized = middleware._normalize_path(path)
        assert normalized == "/api/health"

    def test_exclude_paths_default(self) -> None:
        """Test default excluded paths."""
        middleware = PrometheusMetricsMiddleware(app=None)  # type: ignore[arg-type]
        assert "/health" in middleware._exclude_paths
        assert "/metrics" in middleware._exclude_paths

    def test_exclude_paths_custom(self) -> None:
        """Test custom excluded paths."""
        middleware = PrometheusMetricsMiddleware(
            app=None,  # type: ignore[arg-type]
            exclude_paths=["/health", "/ready", "/internal"],
        )
        assert "/health" in middleware._exclude_paths
        assert "/ready" in middleware._exclude_paths
        assert "/internal" in middleware._exclude_paths
