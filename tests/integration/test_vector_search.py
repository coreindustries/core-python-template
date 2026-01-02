"""Vector search integration tests.

Tests for vector search with mocked AI client and real database.
"""

from unittest.mock import MagicMock

import pytest
from prisma import Prisma

from project_name.models.embedding import EmbeddingCreate, SearchRequest
from project_name.services.vector_search import VectorSearchService


@pytest.mark.integration
@pytest.mark.asyncio
async def test_create_embedding_with_mock_ai(
    db: Prisma,
    patch_ai_client: None,
) -> None:
    """Test creating embedding with mocked AI client.

    Args:
        db: Prisma database client fixture.
        patch_ai_client: Fixture that patches AI client.
    """
    service = VectorSearchService(db)

    embedding = await service.create_embedding(
        EmbeddingCreate(
            content="Test content for vector embedding",
            metadata={"source": "test"},
        )
    )

    try:
        assert embedding.id is not None
        assert embedding.content == "Test content for vector embedding"
        assert embedding.metadata == {"source": "test"}

    finally:
        # Cleanup
        await db.embedding.delete(where={"id": embedding.id})


@pytest.mark.integration
@pytest.mark.asyncio
async def test_search_with_mock_ai(
    db: Prisma,
    patch_ai_client: None,
    mock_ai_client: MagicMock,
) -> None:
    """Test vector search with mocked AI client.

    Args:
        db: Prisma database client fixture.
        patch_ai_client: Fixture that patches AI client.
        mock_ai_client: Mock AI client fixture.
    """
    service = VectorSearchService(db)

    # Create test embedding
    embedding = await service.create_embedding(
        EmbeddingCreate(
            content="Machine learning is a subset of AI",
            metadata={"topic": "ml"},
        )
    )

    try:
        # Perform search
        results = await service.search(
            SearchRequest(
                query="artificial intelligence",
                limit=10,
                threshold=0.0,  # Low threshold for testing
            )
        )

        # With mock returning same vector, similarity should be 1.0
        assert len(results) >= 1
        assert any(r.id == embedding.id for r in results)

        # Verify AI client was called for query embedding
        assert mock_ai_client.embed.call_count >= 1

    finally:
        await db.embedding.delete(where={"id": embedding.id})


@pytest.mark.integration
@pytest.mark.asyncio
async def test_get_embedding(db: Prisma) -> None:
    """Test getting embedding by ID.

    Args:
        db: Prisma database client fixture.
    """
    service = VectorSearchService(db)

    # Create via Prisma directly (no AI needed)
    record = await db.embedding.create(
        data={
            "content": "Test get embedding",
            "metadata": {"test": True},
        }
    )

    try:
        result = await service.get_embedding(record.id)

        assert result is not None
        assert result.id == record.id
        assert result.content == "Test get embedding"

    finally:
        await db.embedding.delete(where={"id": record.id})


@pytest.mark.integration
@pytest.mark.asyncio
async def test_get_embedding_not_found(db: Prisma) -> None:
    """Test getting non-existent embedding.

    Args:
        db: Prisma database client fixture.
    """
    service = VectorSearchService(db)

    result = await service.get_embedding("nonexistent-id")
    assert result is None


@pytest.mark.integration
@pytest.mark.asyncio
async def test_delete_embedding(db: Prisma) -> None:
    """Test deleting embedding.

    Args:
        db: Prisma database client fixture.
    """
    service = VectorSearchService(db)

    # Create via Prisma directly
    record = await db.embedding.create(
        data={
            "content": "Test delete embedding",
        }
    )

    # Delete
    deleted = await service.delete_embedding(record.id)
    assert deleted is True

    # Verify deleted
    result = await service.get_embedding(record.id)
    assert result is None


@pytest.mark.integration
@pytest.mark.asyncio
async def test_delete_embedding_not_found(db: Prisma) -> None:
    """Test deleting non-existent embedding.

    Args:
        db: Prisma database client fixture.
    """
    service = VectorSearchService(db)

    deleted = await service.delete_embedding("nonexistent-id")
    assert deleted is False
