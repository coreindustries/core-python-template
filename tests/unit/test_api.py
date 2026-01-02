"""Tests for API routes."""

import pytest
from httpx import AsyncClient

from project_name import __version__


@pytest.mark.asyncio
async def test_health_check(client: AsyncClient) -> None:
    """Test health check endpoint returns healthy status."""
    response = await client.get("/health")

    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert data["version"] == __version__


@pytest.mark.asyncio
async def test_root_endpoint(client: AsyncClient) -> None:
    """Test root endpoint returns welcome message."""
    response = await client.get("/")

    assert response.status_code == 200
    data = response.json()
    assert "message" in data
