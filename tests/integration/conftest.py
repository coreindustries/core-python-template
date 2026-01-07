"""Integration test fixtures.

Fixtures for database and API integration testing.
"""

from collections.abc import AsyncGenerator
from typing import Any
from unittest.mock import AsyncMock, MagicMock

import pytest
from httpx import ASGITransport, AsyncClient
from prisma import Prisma

from project_name.db import close_db_client, get_db_client
from project_name.main import app


@pytest.fixture
def anyio_backend() -> str:
    """Configure anyio backend for async tests.

    Returns:
        Backend name string.
    """
    return "asyncio"


@pytest.fixture
async def db_client() -> AsyncGenerator[Prisma]:
    """Provide database client for integration tests.

    Function-scoped to match pytest-asyncio event loop scope.

    Yields:
        Prisma database client.
    """
    client = await get_db_client()
    yield client
    await close_db_client()


@pytest.fixture
async def db(db_client: Prisma) -> AsyncGenerator[Prisma]:
    """Provide database client for a single test.

    Uses the session-scoped client but provides test isolation.
    Data created in tests should be cleaned up after use.

    Args:
        db_client: Session-scoped Prisma client.

    Yields:
        Prisma database client.
    """
    yield db_client
    # Note: For true isolation, use transactions or cleanup fixtures
    # await db_client.embedding.delete_many(where={})  # noqa: ERA001


@pytest.fixture
async def integration_client() -> AsyncGenerator[AsyncClient]:
    """Provide HTTP client for API integration tests.

    Uses ASGI transport to test the FastAPI app directly.

    Yields:
        Async HTTP client.
    """
    transport = ASGITransport(app=app)
    async with AsyncClient(
        transport=transport,
        base_url="http://test",
    ) as client:
        yield client


@pytest.fixture
def mock_ai_response() -> dict[str, Any]:
    """Provide mock AI API response data.

    Returns:
        Dictionary with mock embedding response.
    """
    return {
        "embeddings": [[0.1] * 1536],
        "model": "text-embedding-3-small",
        "usage": {
            "prompt_tokens": 10,
            "total_tokens": 10,
        },
    }


@pytest.fixture
def mock_ai_client(mock_ai_response: dict[str, Any]) -> MagicMock:
    """Create a mock AI client for integration tests.

    Avoids making real API calls during testing.

    Args:
        mock_ai_response: Mock response data.

    Returns:
        Mock AI client.
    """
    from project_name.ai.models import EmbeddingResponse, TokenUsage

    mock = MagicMock()
    mock.provider = "openai"

    # Mock embed method
    embed_response = EmbeddingResponse(
        embeddings=mock_ai_response["embeddings"],
        model=mock_ai_response["model"],
        usage=TokenUsage(
            prompt_tokens=mock_ai_response["usage"]["prompt_tokens"],
            total_tokens=mock_ai_response["usage"]["total_tokens"],
        ),
    )
    mock.embed = AsyncMock(return_value=embed_response)

    return mock


@pytest.fixture
def patch_ai_client(mock_ai_client: MagicMock, monkeypatch: pytest.MonkeyPatch) -> None:
    """Patch the AI client factory to return mock.

    Args:
        mock_ai_client: Mock AI client.
        monkeypatch: Pytest monkeypatch fixture.
    """

    def mock_get_client(_provider: str = "openai") -> MagicMock:
        return mock_ai_client

    monkeypatch.setattr("project_name.ai.get_ai_client", mock_get_client)
    monkeypatch.setattr(
        "project_name.services.vector_search.get_ai_client", mock_get_client
    )
