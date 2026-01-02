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
# Database Fixtures - uncomment when needed
# =============================================================================

# from project_name.db import get_db_client, close_db_client

# @pytest.fixture(scope="session")
# def event_loop():
#     """Create event loop for session-scoped fixtures."""
#     import asyncio
#     loop = asyncio.get_event_loop_policy().new_event_loop()
#     yield loop
#     loop.close()

# @pytest.fixture(scope="session")
# async def db():
#     """Provide database client for integration tests."""
#     client = await get_db_client()
#     yield client
#     await close_db_client()

# @pytest.fixture(autouse=True)
# async def clean_db(db):
#     """Clean database before each test."""
#     # Add cleanup logic here
#     yield
#     # Add cleanup logic here
