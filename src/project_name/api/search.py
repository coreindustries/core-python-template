"""Vector search API routes.

Endpoints for semantic search and embedding management.
"""

from fastapi import APIRouter, HTTPException, status

from project_name.ai.exceptions import AIClientError
from project_name.db import get_db
from project_name.models.embedding import (
    EmbeddingCreate,
    EmbeddingResponse,
    SearchRequest,
    SearchResponse,
)
from project_name.services.vector_search import VectorSearchService


router = APIRouter(prefix="/search", tags=["search"])


@router.post(
    "/embeddings",
    response_model=EmbeddingResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_embedding(data: EmbeddingCreate) -> EmbeddingResponse:
    """Create and store a new embedding.

    Generates an embedding vector for the provided content and
    stores it in the database for later similarity search.

    Args:
        data: Embedding creation data with content and optional metadata.

    Returns:
        Created embedding record.

    Raises:
        HTTPException: 503 if AI service is unavailable.
    """
    try:
        async with get_db() as db:
            service = VectorSearchService(db)
            return await service.create_embedding(data)
    except AIClientError as e:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f"AI service error: {e.message}",
        ) from e


@router.post("/", response_model=SearchResponse)
async def search(request: SearchRequest) -> SearchResponse:
    """Perform semantic similarity search.

    Searches for documents similar to the query using
    vector similarity (cosine distance).

    Args:
        request: Search request with query, limit, and threshold.

    Returns:
        Search results with similarity scores.

    Raises:
        HTTPException: 503 if AI service is unavailable.
    """
    try:
        async with get_db() as db:
            service = VectorSearchService(db)
            results = await service.search(request)
            return SearchResponse(
                results=results,
                total=len(results),
                query=request.query,
            )
    except AIClientError as e:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f"AI service error: {e.message}",
        ) from e


@router.get("/embeddings/{embedding_id}", response_model=EmbeddingResponse)
async def get_embedding(embedding_id: str) -> EmbeddingResponse:
    """Get an embedding by ID.

    Args:
        embedding_id: The embedding ID.

    Returns:
        Embedding record.

    Raises:
        HTTPException: 404 if not found.
    """
    async with get_db() as db:
        service = VectorSearchService(db)
        result = await service.get_embedding(embedding_id)
        if result is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Embedding not found",
            )
        return result


@router.delete(
    "/embeddings/{embedding_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_embedding(embedding_id: str) -> None:
    """Delete an embedding by ID.

    Args:
        embedding_id: The embedding ID to delete.

    Raises:
        HTTPException: 404 if not found.
    """
    async with get_db() as db:
        service = VectorSearchService(db)
        deleted = await service.delete_embedding(embedding_id)
        if not deleted:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Embedding not found",
            )
