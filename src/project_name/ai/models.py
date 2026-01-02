"""Pydantic models for AI client operations.

Data models for chat completions and embeddings.
"""

from datetime import UTC, datetime
from enum import Enum
from typing import Any

from pydantic import BaseModel, ConfigDict, Field


class Role(str, Enum):
    """Chat message roles."""

    SYSTEM = "system"
    USER = "user"
    ASSISTANT = "assistant"
    TOOL = "tool"


class ChatMessage(BaseModel):
    """A single chat message.

    Attributes:
        role: The role of the message sender.
        content: The content of the message.
        name: Optional name for the message sender.
    """

    model_config = ConfigDict(use_enum_values=True)

    role: Role
    content: str
    name: str | None = None

    @classmethod
    def system(cls, content: str) -> "ChatMessage":
        """Create a system message.

        Args:
            content: The message content.

        Returns:
            A system ChatMessage.
        """
        return cls(role=Role.SYSTEM, content=content)

    @classmethod
    def user(cls, content: str) -> "ChatMessage":
        """Create a user message.

        Args:
            content: The message content.

        Returns:
            A user ChatMessage.
        """
        return cls(role=Role.USER, content=content)

    @classmethod
    def assistant(cls, content: str) -> "ChatMessage":
        """Create an assistant message.

        Args:
            content: The message content.

        Returns:
            An assistant ChatMessage.
        """
        return cls(role=Role.ASSISTANT, content=content)


class ChatRequest(BaseModel):
    """Chat completion request.

    Attributes:
        messages: List of messages in the conversation.
        model: Model to use for completion.
        temperature: Sampling temperature (0-2).
        max_tokens: Maximum tokens to generate.
        top_p: Nucleus sampling parameter.
        stop: Stop sequences.
        stream: Whether to stream the response.
    """

    messages: list[ChatMessage]
    model: str | None = None
    temperature: float = Field(default=0.7, ge=0, le=2)
    max_tokens: int | None = None
    top_p: float = Field(default=1.0, ge=0, le=1)
    stop: list[str] | None = None
    stream: bool = False


class TokenUsage(BaseModel):
    """Token usage information.

    Attributes:
        prompt_tokens: Tokens in the prompt.
        completion_tokens: Tokens in the completion.
        total_tokens: Total tokens used.
    """

    prompt_tokens: int = 0
    completion_tokens: int = 0
    total_tokens: int = 0


class ChatResponse(BaseModel):
    """Chat completion response.

    Attributes:
        id: Response ID.
        content: Generated content.
        model: Model used.
        usage: Token usage information.
        finish_reason: Reason for completion.
        created_at: When the response was created.
    """

    id: str
    content: str
    model: str
    usage: TokenUsage
    finish_reason: str | None = None
    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))


class EmbeddingRequest(BaseModel):
    """Embedding request.

    Attributes:
        texts: Texts to embed.
        model: Model to use for embedding.
        dimensions: Output dimensions (if model supports it).
    """

    texts: list[str]
    model: str | None = None
    dimensions: int | None = None


class EmbeddingResponse(BaseModel):
    """Embedding response.

    Attributes:
        embeddings: List of embedding vectors.
        model: Model used.
        usage: Token usage information.
    """

    embeddings: list[list[float]]
    model: str
    usage: TokenUsage


class AIMetadata(BaseModel):
    """Metadata for AI operations.

    Attributes:
        provider: AI provider name.
        model: Model used.
        latency_ms: Request latency in milliseconds.
        cached: Whether the response was cached.
        extra: Additional metadata.
    """

    provider: str
    model: str
    latency_ms: float | None = None
    cached: bool = False
    extra: dict[str, Any] = Field(default_factory=dict)
