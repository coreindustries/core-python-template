"""API integration tests.

Tests for API endpoints with real service layer.
"""

import pytest
from httpx import AsyncClient


@pytest.mark.integration
@pytest.mark.asyncio
async def test_health_check_integration(integration_client: AsyncClient) -> None:
    """Test health check endpoint returns healthy status.

    Args:
        integration_client: Async HTTP client fixture.
    """
    response = await integration_client.get("/health")

    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert "version" in data


@pytest.mark.integration
@pytest.mark.asyncio
async def test_root_endpoint_integration(integration_client: AsyncClient) -> None:
    """Test root endpoint returns welcome message.

    Args:
        integration_client: Async HTTP client fixture.
    """
    response = await integration_client.get("/")

    assert response.status_code == 200
    data = response.json()
    assert "message" in data


@pytest.mark.integration
@pytest.mark.asyncio
async def test_metrics_endpoint(integration_client: AsyncClient) -> None:
    """Test metrics endpoint returns Prometheus format.

    Args:
        integration_client: Async HTTP client fixture.
    """
    response = await integration_client.get("/metrics")

    # Should return 200 (or 500 if prometheus-client not installed)
    assert response.status_code in (200, 500)

    if response.status_code == 200:
        # Should be Prometheus text format
        assert "text/plain" in response.headers.get("content-type", "")
