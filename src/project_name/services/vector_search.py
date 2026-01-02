"""Vector search service.

Semantic search using pgvector and OpenAI embeddings.
"""

from typing import Any, cast

from prisma import Prisma

from project_name.ai import EmbeddingRequest, get_ai_client
from project_name.ai.exceptions import AIClientError
from project_name.logging import get_audit_logger, get_logger
from project_name.logging.audit import AuditAction
from project_name.models.embedding import (
    EmbeddingCreate,
    EmbeddingResponse,
    SearchRequest,
    SearchResult,
)


logger = get_logger(__name__)
audit = get_audit_logger()


class VectorSearchService:
    """Service for vector-based semantic search.

    Uses pgvector for similarity search with OpenAI embeddings.

    Example:
        >>> async with get_db() as db:
        ...     service = VectorSearchService(db)
        ...     results = await service.search(
        ...         SearchRequest(query="machine learning")
        ...     )
    """

    def __init__(self, db: Prisma) -> None:
        """Initialize the vector search service.

        Args:
            db: Prisma database client.
        """
        self._db = db

    async def create_embedding(
        self,
        data: EmbeddingCreate,
        user_id: str = "system",
    ) -> EmbeddingResponse:
        """Create and store an embedding.

        Generates an embedding vector using the AI client and stores
        it in the database with the original content.

        Args:
            data: Embedding creation data with content and metadata.
            user_id: ID of the user creating the embedding.

        Returns:
            Created embedding record.

        Raises:
            AIClientError: If embedding generation fails.
        """
        # Generate embedding vector
        try:
            ai_client = get_ai_client()
            embedding_response = await ai_client.embed(
                EmbeddingRequest(texts=[data.content])
            )
            vector = embedding_response.embeddings[0]
        except AIClientError:
            logger.exception("Failed to generate embedding")
            raise

        # Store in database
        # First create the Prisma record
        record = await self._db.embedding.create(
            data={
                "content": data.content,
                "metadata": cast(Any, data.metadata),
            }
        )

        # Then add the vector column via raw SQL
        vector_str = "[" + ",".join(str(v) for v in vector) + "]"
        await self._db.execute_raw(
            """
            UPDATE embeddings
            SET embedding = $1::vector
            WHERE id = $2
            """,
            vector_str,
            record.id,
        )

        # Log the data access
        audit.data_access(
            user_id=user_id,
            resource_type="embedding",
            resource_id=record.id,
            action=AuditAction.DATA_CREATE,
        )

        logger.info(
            "Embedding created",
            extra={
                "embedding_id": record.id,
                "content_length": len(data.content),
            },
        )

        return EmbeddingResponse(
            id=record.id,
            content=record.content,
            metadata=cast(dict[str, Any] | None, record.metadata),
            created_at=record.createdAt,
            updated_at=record.updatedAt,
        )

    async def search(
        self,
        request: SearchRequest,
        user_id: str = "system",
    ) -> list[SearchResult]:
        """Perform semantic similarity search.

        Generates an embedding for the query and finds similar
        documents using cosine similarity.

        Args:
            request: Search request with query and parameters.
            user_id: ID of the user performing the search.

        Returns:
            List of search results ordered by similarity.

        Raises:
            AIClientError: If query embedding generation fails.
        """
        # Generate query embedding
        try:
            ai_client = get_ai_client()
            embedding_response = await ai_client.embed(
                EmbeddingRequest(texts=[request.query])
            )
            query_vector = embedding_response.embeddings[0]
        except AIClientError:
            logger.exception("Failed to generate query embedding")
            raise

        # Perform similarity search using raw SQL
        vector_str = "[" + ",".join(str(v) for v in query_vector) + "]"

        results: list[dict[str, Any]] = await self._db.query_raw(
            """
            SELECT
                id,
                content,
                metadata,
                1 - (embedding <=> $1::vector) as similarity
            FROM embeddings
            WHERE embedding IS NOT NULL
              AND 1 - (embedding <=> $1::vector) >= $2
            ORDER BY embedding <=> $1::vector
            LIMIT $3
            """,
            vector_str,
            request.threshold,
            request.limit,
        )

        # Log the search
        audit.data_access(
            user_id=user_id,
            resource_type="embedding",
            action=AuditAction.DATA_READ,
            metadata={
                "query_length": len(request.query),
                "results_count": len(results),
            },
        )

        logger.info(
            "Vector search completed",
            extra={
                "query_length": len(request.query),
                "threshold": request.threshold,
                "limit": request.limit,
                "results_count": len(results),
            },
        )

        return [
            SearchResult(
                id=row["id"],
                content=row["content"],
                similarity=float(row["similarity"]),
                metadata=row.get("metadata"),
            )
            for row in results
        ]

    async def get_embedding(self, embedding_id: str) -> EmbeddingResponse | None:
        """Get an embedding by ID.

        Args:
            embedding_id: The embedding ID.

        Returns:
            Embedding record or None if not found.
        """
        record = await self._db.embedding.find_unique(
            where={"id": embedding_id}
        )

        if record is None:
            return None

        return EmbeddingResponse(
            id=record.id,
            content=record.content,
            metadata=cast(dict[str, Any] | None, record.metadata),
            created_at=record.createdAt,
            updated_at=record.updatedAt,
        )

    async def delete_embedding(
        self,
        embedding_id: str,
        user_id: str = "system",
    ) -> bool:
        """Delete an embedding by ID.

        Args:
            embedding_id: The embedding ID to delete.
            user_id: ID of the user deleting the embedding.

        Returns:
            True if deleted, False if not found.
        """
        try:
            await self._db.embedding.delete(
                where={"id": embedding_id}
            )

            audit.data_access(
                user_id=user_id,
                resource_type="embedding",
                resource_id=embedding_id,
                action=AuditAction.DATA_DELETE,
            )

            logger.info(
                "Embedding deleted",
                extra={"embedding_id": embedding_id},
            )
            return True

        except Exception:
            logger.debug(
                "Embedding not found for deletion",
                extra={"embedding_id": embedding_id},
            )
            return False
