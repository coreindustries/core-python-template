"""Database integration tests.

Tests for database operations with real PostgreSQL.
"""

import pytest
from prisma import Prisma


@pytest.mark.integration
@pytest.mark.asyncio
async def test_database_connection(db: Prisma) -> None:
    """Test database connection is working.

    Args:
        db: Prisma database client fixture.
    """
    # Simple query to verify connection
    assert db.is_connected()


@pytest.mark.integration
@pytest.mark.asyncio
async def test_embedding_crud_operations(db: Prisma) -> None:
    """Test embedding CRUD operations with real database.

    Args:
        db: Prisma database client fixture.
    """
    # Create
    embedding = await db.embedding.create(
        data={
            "content": "Test content for integration testing",
            "metadata": {"source": "integration_test", "version": 1},
        }
    )

    assert embedding.id is not None
    assert embedding.content == "Test content for integration testing"
    assert embedding.metadata == {"source": "integration_test", "version": 1}

    # Read
    found = await db.embedding.find_unique(where={"id": embedding.id})
    assert found is not None
    assert found.content == embedding.content
    assert found.metadata == embedding.metadata

    # Update
    updated = await db.embedding.update(
        where={"id": embedding.id},
        data={"content": "Updated test content"},
    )
    assert updated.content == "Updated test content"

    # Delete
    deleted = await db.embedding.delete(where={"id": embedding.id})
    assert deleted.id == embedding.id

    # Verify deleted
    not_found = await db.embedding.find_unique(where={"id": embedding.id})
    assert not_found is None


@pytest.mark.integration
@pytest.mark.asyncio
async def test_embedding_metadata_json(db: Prisma) -> None:
    """Test embedding metadata JSON operations.

    Args:
        db: Prisma database client fixture.
    """
    # Create with complex metadata
    metadata = {
        "tags": ["test", "integration"],
        "nested": {"key": "value"},
        "count": 42,
    }

    embedding = await db.embedding.create(
        data={
            "content": "Content with complex metadata",
            "metadata": metadata,
        }
    )

    try:
        # Verify metadata preserved
        found = await db.embedding.find_unique(where={"id": embedding.id})
        assert found is not None
        assert found.metadata == metadata

    finally:
        # Cleanup
        await db.embedding.delete(where={"id": embedding.id})


@pytest.mark.integration
@pytest.mark.asyncio
async def test_embedding_null_metadata(db: Prisma) -> None:
    """Test embedding with null metadata.

    Args:
        db: Prisma database client fixture.
    """
    embedding = await db.embedding.create(
        data={
            "content": "Content without metadata",
            "metadata": None,
        }
    )

    try:
        found = await db.embedding.find_unique(where={"id": embedding.id})
        assert found is not None
        assert found.metadata is None

    finally:
        await db.embedding.delete(where={"id": embedding.id})
