"""Tests for OpenAI client."""

from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from project_name.ai.clients.openai import OpenAIClient
from project_name.ai.config import AISettings
from project_name.ai.exceptions import (
    AIClientError,
    AuthenticationError,
    ContextLengthExceededError,
    InvalidRequestError,
    RateLimitError,
)
from project_name.ai.models import ChatMessage, ChatRequest, EmbeddingRequest


class TestOpenAIClientInit:
    """Tests for OpenAIClient initialization."""

    def test_init_without_api_key_raises_error(self) -> None:
        """Test that initialization without API key raises AuthenticationError."""
        settings = AISettings()  # No API key
        with pytest.raises(AuthenticationError, match="API key not configured"):
            OpenAIClient(settings=settings)

    def test_init_with_api_key_succeeds(self) -> None:
        """Test that initialization with API key succeeds."""
        settings = AISettings(openai_api_key="sk-test-key")  # type: ignore[arg-type]
        client = OpenAIClient(settings=settings)
        assert client.provider == "openai"


class TestOpenAIClientChat:
    """Tests for OpenAI chat completions."""

    @pytest.fixture
    def client(self) -> OpenAIClient:
        """Create a client with mock settings."""
        settings = AISettings(openai_api_key="sk-test-key")  # type: ignore[arg-type]
        return OpenAIClient(settings=settings)

    @pytest.fixture
    def mock_response(self) -> MagicMock:
        """Create a mock chat completion response."""
        response = MagicMock()
        response.id = "chatcmpl-123"
        response.model = "gpt-4o-mini"
        response.choices = [
            MagicMock(
                message=MagicMock(content="Hello! How can I help?"),
                finish_reason="stop",
            )
        ]
        response.usage = MagicMock(
            prompt_tokens=10,
            completion_tokens=20,
            total_tokens=30,
        )
        return response

    @pytest.mark.asyncio
    async def test_chat_success(
        self, client: OpenAIClient, mock_response: MagicMock
    ) -> None:
        """Test successful chat completion."""
        with patch.object(client, "_get_client") as mock_get_client:
            mock_client = AsyncMock()
            mock_client.chat.completions.create = AsyncMock(return_value=mock_response)
            mock_get_client.return_value = mock_client

            request = ChatRequest(
                messages=[ChatMessage.user("Hello!")],
            )
            response = await client.chat(request)

            assert response.id == "chatcmpl-123"
            assert response.content == "Hello! How can I help?"
            assert response.usage.total_tokens == 30

    @pytest.mark.asyncio
    async def test_chat_rate_limit_error(self, client: OpenAIClient) -> None:
        """Test rate limit error handling."""
        with patch.object(client, "_get_client") as mock_get_client:
            mock_client = AsyncMock()
            mock_client.chat.completions.create = AsyncMock(
                side_effect=Exception("Rate limit exceeded (429)")
            )
            mock_get_client.return_value = mock_client

            request = ChatRequest(
                messages=[ChatMessage.user("Hello!")],
            )

            with pytest.raises(RateLimitError):
                await client.chat(request)

    @pytest.mark.asyncio
    async def test_chat_authentication_error(self, client: OpenAIClient) -> None:
        """Test authentication error handling."""
        with patch.object(client, "_get_client") as mock_get_client:
            mock_client = AsyncMock()
            mock_client.chat.completions.create = AsyncMock(
                side_effect=Exception("Authentication failed (401)")
            )
            mock_get_client.return_value = mock_client

            request = ChatRequest(
                messages=[ChatMessage.user("Hello!")],
            )

            with pytest.raises(AuthenticationError):
                await client.chat(request)

    @pytest.mark.asyncio
    async def test_chat_context_length_error(self, client: OpenAIClient) -> None:
        """Test context length exceeded error handling."""
        with patch.object(client, "_get_client") as mock_get_client:
            mock_client = AsyncMock()
            mock_client.chat.completions.create = AsyncMock(
                side_effect=Exception("maximum context length exceeded")
            )
            mock_get_client.return_value = mock_client

            request = ChatRequest(
                messages=[ChatMessage.user("Hello!")],
            )

            with pytest.raises(ContextLengthExceededError):
                await client.chat(request)

    @pytest.mark.asyncio
    async def test_chat_invalid_request_error(self, client: OpenAIClient) -> None:
        """Test invalid request error handling."""
        with patch.object(client, "_get_client") as mock_get_client:
            mock_client = AsyncMock()
            mock_client.chat.completions.create = AsyncMock(
                side_effect=Exception("Invalid request (400)")
            )
            mock_get_client.return_value = mock_client

            request = ChatRequest(
                messages=[ChatMessage.user("Hello!")],
            )

            with pytest.raises(InvalidRequestError):
                await client.chat(request)

    @pytest.mark.asyncio
    async def test_chat_generic_error(self, client: OpenAIClient) -> None:
        """Test generic error handling."""
        with patch.object(client, "_get_client") as mock_get_client:
            mock_client = AsyncMock()
            mock_client.chat.completions.create = AsyncMock(
                side_effect=Exception("Unknown error")
            )
            mock_get_client.return_value = mock_client

            request = ChatRequest(
                messages=[ChatMessage.user("Hello!")],
            )

            with pytest.raises(AIClientError):
                await client.chat(request)


class TestOpenAIClientStream:
    """Tests for OpenAI streaming chat completions."""

    @pytest.fixture
    def client(self) -> OpenAIClient:
        """Create a client with mock settings."""
        settings = AISettings(openai_api_key="sk-test-key")  # type: ignore[arg-type]
        return OpenAIClient(settings=settings)

    @pytest.mark.asyncio
    async def test_chat_stream_success(self, client: OpenAIClient) -> None:
        """Test successful streaming chat completion."""

        async def mock_stream() -> AsyncMock:
            """Create mock stream chunks."""
            chunks = [
                MagicMock(choices=[MagicMock(delta=MagicMock(content="Hello"))]),
                MagicMock(choices=[MagicMock(delta=MagicMock(content=" world"))]),
                MagicMock(choices=[MagicMock(delta=MagicMock(content="!"))]),
            ]
            for chunk in chunks:
                yield chunk

        with patch.object(client, "_get_client") as mock_get_client:
            mock_client = AsyncMock()
            mock_client.chat.completions.create = AsyncMock(return_value=mock_stream())
            mock_get_client.return_value = mock_client

            request = ChatRequest(
                messages=[ChatMessage.user("Hello!")],
            )

            chunks = []
            async for chunk in client.chat_stream(request):
                chunks.append(chunk)

            assert chunks == ["Hello", " world", "!"]

    @pytest.mark.asyncio
    async def test_chat_stream_error(self, client: OpenAIClient) -> None:
        """Test streaming error handling."""
        with patch.object(client, "_get_client") as mock_get_client:
            mock_client = AsyncMock()
            mock_client.chat.completions.create = AsyncMock(
                side_effect=Exception("Rate limit exceeded")
            )
            mock_get_client.return_value = mock_client

            request = ChatRequest(
                messages=[ChatMessage.user("Hello!")],
            )

            with pytest.raises(RateLimitError):
                async for _ in client.chat_stream(request):
                    pass


class TestOpenAIClientEmbed:
    """Tests for OpenAI embeddings."""

    @pytest.fixture
    def client(self) -> OpenAIClient:
        """Create a client with mock settings."""
        settings = AISettings(openai_api_key="sk-test-key")  # type: ignore[arg-type]
        return OpenAIClient(settings=settings)

    @pytest.fixture
    def mock_embedding_response(self) -> MagicMock:
        """Create a mock embedding response."""
        response = MagicMock()
        response.model = "text-embedding-3-small"
        response.data = [
            MagicMock(embedding=[0.1, 0.2, 0.3]),
        ]
        response.usage = MagicMock(
            prompt_tokens=5,
            total_tokens=5,
        )
        return response

    @pytest.mark.asyncio
    async def test_embed_success(
        self, client: OpenAIClient, mock_embedding_response: MagicMock
    ) -> None:
        """Test successful embedding generation."""
        with patch.object(client, "_get_client") as mock_get_client:
            mock_client = AsyncMock()
            mock_client.embeddings.create = AsyncMock(
                return_value=mock_embedding_response
            )
            mock_get_client.return_value = mock_client

            request = EmbeddingRequest(texts=["Hello world"])
            response = await client.embed(request)

            assert response.model == "text-embedding-3-small"
            assert len(response.embeddings) == 1
            assert response.embeddings[0] == [0.1, 0.2, 0.3]
            assert response.usage.prompt_tokens == 5

    @pytest.mark.asyncio
    async def test_embed_error(self, client: OpenAIClient) -> None:
        """Test embedding error handling."""
        with patch.object(client, "_get_client") as mock_get_client:
            mock_client = AsyncMock()
            mock_client.embeddings.create = AsyncMock(
                side_effect=Exception("Rate limit exceeded")
            )
            mock_get_client.return_value = mock_client

            request = EmbeddingRequest(texts=["Hello world"])

            with pytest.raises(RateLimitError):
                await client.embed(request)


class TestOpenAIClientLifecycle:
    """Tests for OpenAI client lifecycle."""

    @pytest.fixture
    def client(self) -> OpenAIClient:
        """Create a client with mock settings."""
        settings = AISettings(openai_api_key="sk-test-key")  # type: ignore[arg-type]
        return OpenAIClient(settings=settings)

    @pytest.mark.asyncio
    async def test_close(self, client: OpenAIClient) -> None:
        """Test client close."""
        # Set up a mock client directly
        mock_instance = AsyncMock()
        client._client = mock_instance

        # Close the client
        await client.close()

        mock_instance.close.assert_called_once()
        assert client._client is None

    @pytest.mark.asyncio
    async def test_close_when_not_initialized(self, client: OpenAIClient) -> None:
        """Test client close when not initialized."""
        # Just ensure no error is raised
        await client.close()
        assert client._client is None

    def test_get_client_creates_client(self, client: OpenAIClient) -> None:
        """Test that _get_client creates the OpenAI client."""
        with patch("openai.AsyncOpenAI") as mock_class:
            mock_instance = MagicMock()
            mock_class.return_value = mock_instance

            result = client._get_client()

            assert result is mock_instance
            mock_class.assert_called_once()

    def test_get_client_reuses_client(self, client: OpenAIClient) -> None:
        """Test that _get_client reuses existing client."""
        # Set up an existing client
        mock_instance = MagicMock()
        client._client = mock_instance

        result1 = client._get_client()
        result2 = client._get_client()

        assert result1 is result2
        assert result1 is mock_instance

    def test_get_client_import_error(self, client: OpenAIClient) -> None:
        """Test that _get_client handles import error."""
        # Reset the client
        client._client = None

        with (
            patch.dict("sys.modules", {"openai": None}),
            pytest.raises(AIClientError, match="openai package not installed"),
        ):
            client._get_client()


class TestOpenAIClientContextManager:
    """Tests for OpenAI client context manager."""

    @pytest.mark.asyncio
    async def test_async_context_manager(self) -> None:
        """Test async context manager usage."""
        settings = AISettings(openai_api_key="sk-test-key")  # type: ignore[arg-type]

        mock_instance = AsyncMock()

        async with OpenAIClient(settings=settings) as client:
            assert client.provider == "openai"
            # Set a mock client directly
            client._client = mock_instance

        # Verify close was called
        mock_instance.close.assert_called_once()
