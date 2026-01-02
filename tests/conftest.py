"""Pytest configuration and fixtures.

This module provides shared fixtures for all tests.
"""

from collections.abc import AsyncGenerator

import pytest
from httpx import ASGITransport, AsyncClient

from project_name.main import app


@pytest.fixture
def anyio_backend() -> str:
    """Configure anyio backend for async tests."""
    return "asyncio"


@pytest.fixture
async def client() -> AsyncGenerator[AsyncClient, None]:
    """Provide async HTTP client for API testing.

    Yields:
        AsyncClient configured for the test application.
    """
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac


# =============================================================================
# Database Fixtures
# =============================================================================
# To add database fixtures for integration tests:
# 1. Import: from project_name.db import get_db_client, close_db_client
# 2. Create session-scoped fixtures for database connections
# 3. Use autouse fixtures for test cleanup
