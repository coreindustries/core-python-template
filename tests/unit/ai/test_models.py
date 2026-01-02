"""Tests for AI models."""

import pytest
from pydantic import ValidationError

from project_name.ai.models import (
    ChatMessage,
    ChatRequest,
    ChatResponse,
    EmbeddingRequest,
    EmbeddingResponse,
    Role,
    TokenUsage,
)


class TestChatMessage:
    """Tests for ChatMessage model."""

    def test_create_user_message(self) -> None:
        """Test creating a user message."""
        msg = ChatMessage.user("Hello!")
        assert msg.role == Role.USER
        assert msg.content == "Hello!"
        assert msg.name is None

    def test_create_system_message(self) -> None:
        """Test creating a system message."""
        msg = ChatMessage.system("You are helpful.")
        assert msg.role == Role.SYSTEM
        assert msg.content == "You are helpful."

    def test_create_assistant_message(self) -> None:
        """Test creating an assistant message."""
        msg = ChatMessage.assistant("Hi there!")
        assert msg.role == Role.ASSISTANT
        assert msg.content == "Hi there!"

    def test_message_with_name(self) -> None:
        """Test message with name."""
        msg = ChatMessage(role=Role.USER, content="Test", name="Alice")
        assert msg.name == "Alice"


class TestChatRequest:
    """Tests for ChatRequest model."""

    def test_default_values(self) -> None:
        """Test default request values."""
        msg = ChatMessage.user("Test")
        request = ChatRequest(messages=[msg])

        assert request.model is None
        assert request.temperature == 0.7
        assert request.max_tokens is None
        assert request.top_p == 1.0
        assert request.stream is False

    def test_custom_values(self) -> None:
        """Test custom request values."""
        msg = ChatMessage.user("Test")
        request = ChatRequest(
            messages=[msg],
            model="gpt-4o",
            temperature=0.5,
            max_tokens=100,
        )

        assert request.model == "gpt-4o"
        assert request.temperature == 0.5
        assert request.max_tokens == 100

    def test_temperature_validation(self) -> None:
        """Test temperature validation bounds."""
        msg = ChatMessage.user("Test")

        with pytest.raises(ValidationError):
            ChatRequest(messages=[msg], temperature=-0.1)

        with pytest.raises(ValidationError):
            ChatRequest(messages=[msg], temperature=2.1)


class TestTokenUsage:
    """Tests for TokenUsage model."""

    def test_default_values(self) -> None:
        """Test default token usage."""
        usage = TokenUsage()
        assert usage.prompt_tokens == 0
        assert usage.completion_tokens == 0
        assert usage.total_tokens == 0

    def test_custom_values(self) -> None:
        """Test custom token usage."""
        usage = TokenUsage(
            prompt_tokens=100,
            completion_tokens=50,
            total_tokens=150,
        )
        assert usage.prompt_tokens == 100
        assert usage.completion_tokens == 50
        assert usage.total_tokens == 150


class TestChatResponse:
    """Tests for ChatResponse model."""

    def test_response_creation(self) -> None:
        """Test chat response creation."""
        response = ChatResponse(
            id="test-123",
            content="Hello!",
            model="gpt-4o-mini",
            usage=TokenUsage(total_tokens=10),
        )

        assert response.id == "test-123"
        assert response.content == "Hello!"
        assert response.model == "gpt-4o-mini"
        assert response.created_at is not None


class TestEmbeddingRequest:
    """Tests for EmbeddingRequest model."""

    def test_single_text(self) -> None:
        """Test single text embedding request."""
        request = EmbeddingRequest(texts=["Hello"])
        assert len(request.texts) == 1
        assert request.model is None
        assert request.dimensions is None

    def test_multiple_texts(self) -> None:
        """Test multiple text embedding request."""
        request = EmbeddingRequest(
            texts=["Hello", "World"],
            model="text-embedding-3-small",
            dimensions=1536,
        )
        assert len(request.texts) == 2
        assert request.model == "text-embedding-3-small"
        assert request.dimensions == 1536


class TestEmbeddingResponse:
    """Tests for EmbeddingResponse model."""

    def test_response_creation(self) -> None:
        """Test embedding response creation."""
        response = EmbeddingResponse(
            embeddings=[[0.1, 0.2, 0.3]],
            model="text-embedding-3-small",
            usage=TokenUsage(prompt_tokens=5),
        )

        assert len(response.embeddings) == 1
        assert response.model == "text-embedding-3-small"
        assert response.usage.prompt_tokens == 5
