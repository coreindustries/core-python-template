"""Pydantic models for embedding and vector search.

Data models for vector storage and semantic search operations.
"""

from datetime import datetime
from typing import Any

from pydantic import Field

from project_name.models import BaseSchema


class EmbeddingBase(BaseSchema):
    """Base embedding schema.

    Attributes:
        content: Text content to embed.
        metadata: Optional metadata for the embedding.
    """

    content: str = Field(min_length=1, max_length=100000)
    metadata: dict[str, Any] | None = None


class EmbeddingCreate(EmbeddingBase):
    """Schema for creating an embedding.

    Inherits content and metadata from EmbeddingBase.
    """

    pass


class EmbeddingResponse(EmbeddingBase):
    """Schema for embedding responses.

    Attributes:
        id: Unique identifier.
        content: Text content.
        metadata: Optional metadata.
        created_at: Creation timestamp.
        updated_at: Last update timestamp.
    """

    id: str
    created_at: datetime
    updated_at: datetime


class SearchRequest(BaseSchema):
    """Schema for vector search request.

    Attributes:
        query: Search query text.
        limit: Maximum number of results to return.
        threshold: Minimum similarity threshold (0-1).
    """

    query: str = Field(min_length=1, max_length=10000)
    limit: int = Field(default=10, ge=1, le=100)
    threshold: float = Field(default=0.7, ge=0.0, le=1.0)


class SearchResult(BaseSchema):
    """Schema for a single search result.

    Attributes:
        id: Embedding ID.
        content: Original text content.
        similarity: Cosine similarity score (0-1).
        metadata: Optional embedding metadata.
    """

    id: str
    content: str
    similarity: float = Field(ge=0.0, le=1.0)
    metadata: dict[str, Any] | None = None


class SearchResponse(BaseSchema):
    """Schema for search response.

    Attributes:
        results: List of search results.
        total: Total number of results found.
        query: Original search query.
    """

    results: list[SearchResult]
    total: int
    query: str
