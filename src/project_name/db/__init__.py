"""Database utilities and connection management.

This module provides database connection handling using Prisma.
"""

from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from prisma import Prisma  # type: ignore[attr-defined]


# Global database client instance
_db: Prisma | None = None


async def get_db_client() -> Prisma:
    """Get or create the database client.

    Returns:
        Prisma database client.
    """
    global _db  # noqa: PLW0603
    if _db is None:
        _db = Prisma()
    if not _db.is_connected():
        await _db.connect()
    return _db


async def close_db_client() -> None:
    """Close the database client connection."""
    global _db  # noqa: PLW0603
    if _db is not None and _db.is_connected():
        await _db.disconnect()
        _db = None


@asynccontextmanager
async def get_db() -> AsyncGenerator[Prisma, None]:
    """Context manager for database operations.

    Provides a database client that is automatically connected.

    Yields:
        Connected Prisma client.

    Example:
        async with get_db() as db:
            user = await db.user.find_unique(where={"id": "123"})
    """
    db = await get_db_client()
    try:
        yield db
    finally:
        # Don't disconnect here - let the connection be reused
        # Connection cleanup happens in close_db_client()
        pass
