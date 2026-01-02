"""Tests for search API endpoints."""

from datetime import UTC, datetime
from unittest.mock import AsyncMock, patch

import pytest
from fastapi.testclient import TestClient

from project_name.ai.exceptions import AIClientError
from project_name.main import app
from project_name.models.embedding import EmbeddingResponse, SearchResult


@pytest.fixture
def client() -> TestClient:
    """Create test client."""
    return TestClient(app, raise_server_exceptions=False)


class TestCreateEmbedding:
    """Tests for POST /search/embeddings."""

    def test_create_embedding_success(self, client: TestClient) -> None:
        """Test successful embedding creation."""
        mock_response = EmbeddingResponse(
            id="cuid123",
            content="test content",
            metadata={"key": "value"},
            created_at=datetime.now(UTC),
            updated_at=datetime.now(UTC),
        )

        with patch("project_name.api.search.get_db") as mock_get_db:
            mock_db = AsyncMock()
            mock_get_db.return_value.__aenter__.return_value = mock_db

            with patch(
                "project_name.api.search.VectorSearchService"
            ) as mock_service_class:
                mock_service = AsyncMock()
                mock_service.create_embedding.return_value = mock_response
                mock_service_class.return_value = mock_service

                response = client.post(
                    "/search/embeddings",
                    json={"content": "test content", "metadata": {"key": "value"}},
                )

                assert response.status_code == 201
                data = response.json()
                assert data["id"] == "cuid123"
                assert data["content"] == "test content"

    def test_create_embedding_ai_error(self, client: TestClient) -> None:
        """Test embedding creation with AI service error."""
        with patch("project_name.api.search.get_db") as mock_get_db:
            mock_db = AsyncMock()
            mock_get_db.return_value.__aenter__.return_value = mock_db

            with patch(
                "project_name.api.search.VectorSearchService"
            ) as mock_service_class:
                mock_service = AsyncMock()
                mock_service.create_embedding.side_effect = AIClientError(
                    message="API error", provider="openai"
                )
                mock_service_class.return_value = mock_service

                response = client.post(
                    "/search/embeddings",
                    json={"content": "test content"},
                )

                assert response.status_code == 503
                assert "AI service error" in response.json()["detail"]


class TestSearch:
    """Tests for POST /search/."""

    def test_search_success(self, client: TestClient) -> None:
        """Test successful search."""
        mock_results = [
            SearchResult(
                id="cuid1",
                content="result 1",
                similarity=0.95,
                metadata=None,
            ),
            SearchResult(
                id="cuid2",
                content="result 2",
                similarity=0.85,
                metadata={"tag": "test"},
            ),
        ]

        with patch("project_name.api.search.get_db") as mock_get_db:
            mock_db = AsyncMock()
            mock_get_db.return_value.__aenter__.return_value = mock_db

            with patch(
                "project_name.api.search.VectorSearchService"
            ) as mock_service_class:
                mock_service = AsyncMock()
                mock_service.search.return_value = mock_results
                mock_service_class.return_value = mock_service

                response = client.post(
                    "/search/",
                    json={"query": "test query", "limit": 10, "threshold": 0.5},
                )

                assert response.status_code == 200
                data = response.json()
                assert data["total"] == 2
                assert data["query"] == "test query"
                assert len(data["results"]) == 2
                assert data["results"][0]["similarity"] == 0.95

    def test_search_empty_results(self, client: TestClient) -> None:
        """Test search with no results."""
        with patch("project_name.api.search.get_db") as mock_get_db:
            mock_db = AsyncMock()
            mock_get_db.return_value.__aenter__.return_value = mock_db

            with patch(
                "project_name.api.search.VectorSearchService"
            ) as mock_service_class:
                mock_service = AsyncMock()
                mock_service.search.return_value = []
                mock_service_class.return_value = mock_service

                response = client.post(
                    "/search/",
                    json={"query": "no matches"},
                )

                assert response.status_code == 200
                data = response.json()
                assert data["total"] == 0
                assert data["results"] == []

    def test_search_ai_error(self, client: TestClient) -> None:
        """Test search with AI service error."""
        with patch("project_name.api.search.get_db") as mock_get_db:
            mock_db = AsyncMock()
            mock_get_db.return_value.__aenter__.return_value = mock_db

            with patch(
                "project_name.api.search.VectorSearchService"
            ) as mock_service_class:
                mock_service = AsyncMock()
                mock_service.search.side_effect = AIClientError(
                    message="Rate limit", provider="openai"
                )
                mock_service_class.return_value = mock_service

                response = client.post(
                    "/search/",
                    json={"query": "test query"},
                )

                assert response.status_code == 503
                assert "AI service error" in response.json()["detail"]


class TestGetEmbedding:
    """Tests for GET /search/embeddings/{embedding_id}."""

    def test_get_embedding_success(self, client: TestClient) -> None:
        """Test successful embedding retrieval."""
        mock_response = EmbeddingResponse(
            id="cuid123",
            content="test content",
            metadata=None,
            created_at=datetime.now(UTC),
            updated_at=datetime.now(UTC),
        )

        with patch("project_name.api.search.get_db") as mock_get_db:
            mock_db = AsyncMock()
            mock_get_db.return_value.__aenter__.return_value = mock_db

            with patch(
                "project_name.api.search.VectorSearchService"
            ) as mock_service_class:
                mock_service = AsyncMock()
                mock_service.get_embedding.return_value = mock_response
                mock_service_class.return_value = mock_service

                response = client.get("/search/embeddings/cuid123")

                assert response.status_code == 200
                data = response.json()
                assert data["id"] == "cuid123"
                assert data["content"] == "test content"

    def test_get_embedding_not_found(self, client: TestClient) -> None:
        """Test embedding not found."""
        with patch("project_name.api.search.get_db") as mock_get_db:
            mock_db = AsyncMock()
            mock_get_db.return_value.__aenter__.return_value = mock_db

            with patch(
                "project_name.api.search.VectorSearchService"
            ) as mock_service_class:
                mock_service = AsyncMock()
                mock_service.get_embedding.return_value = None
                mock_service_class.return_value = mock_service

                response = client.get("/search/embeddings/nonexistent")

                assert response.status_code == 404
                assert response.json()["detail"] == "Embedding not found"


class TestDeleteEmbedding:
    """Tests for DELETE /search/embeddings/{embedding_id}."""

    def test_delete_embedding_success(self, client: TestClient) -> None:
        """Test successful embedding deletion."""
        with patch("project_name.api.search.get_db") as mock_get_db:
            mock_db = AsyncMock()
            mock_get_db.return_value.__aenter__.return_value = mock_db

            with patch(
                "project_name.api.search.VectorSearchService"
            ) as mock_service_class:
                mock_service = AsyncMock()
                mock_service.delete_embedding.return_value = True
                mock_service_class.return_value = mock_service

                response = client.delete("/search/embeddings/cuid123")

                assert response.status_code == 204

    def test_delete_embedding_not_found(self, client: TestClient) -> None:
        """Test deletion of non-existent embedding."""
        with patch("project_name.api.search.get_db") as mock_get_db:
            mock_db = AsyncMock()
            mock_get_db.return_value.__aenter__.return_value = mock_db

            with patch(
                "project_name.api.search.VectorSearchService"
            ) as mock_service_class:
                mock_service = AsyncMock()
                mock_service.delete_embedding.return_value = False
                mock_service_class.return_value = mock_service

                response = client.delete("/search/embeddings/nonexistent")

                assert response.status_code == 404
                assert response.json()["detail"] == "Embedding not found"
