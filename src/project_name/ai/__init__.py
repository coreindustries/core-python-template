"""AI client module.

Abstraction layer for LLM providers with token tracking and prompt templates.

Example:
    >>> from project_name.ai import get_ai_client, ChatMessage
    >>>
    >>> async with get_ai_client() as client:
    ...     response = await client.chat(ChatRequest(
    ...         messages=[ChatMessage.user("Hello, world!")],
    ...     ))
    ...     print(response.content)
"""

from project_name.ai.base import BaseLLMClient
from project_name.ai.clients.openai import OpenAIClient
from project_name.ai.config import AISettings, get_ai_settings
from project_name.ai.exceptions import (
    AIClientError,
    AuthenticationError,
    ContextLengthExceededError,
    InvalidRequestError,
    ModelNotFoundError,
    RateLimitError,
)
from project_name.ai.models import (
    ChatMessage,
    ChatRequest,
    ChatResponse,
    EmbeddingRequest,
    EmbeddingResponse,
    Role,
    TokenUsage,
)
from project_name.ai.prompts import PromptTemplate
from project_name.ai.tracking import (
    TokenTracker,
    TokenUsageRecord,
    get_token_tracker,
)


__all__ = [
    "AIClientError",
    "AISettings",
    "AuthenticationError",
    "BaseLLMClient",
    "ChatMessage",
    "ChatRequest",
    "ChatResponse",
    "ContextLengthExceededError",
    "EmbeddingRequest",
    "EmbeddingResponse",
    "InvalidRequestError",
    "ModelNotFoundError",
    "OpenAIClient",
    "PromptTemplate",
    "RateLimitError",
    "Role",
    "TokenTracker",
    "TokenUsage",
    "TokenUsageRecord",
    "close_ai_client",
    "get_ai_client",
    "get_ai_settings",
    "get_token_tracker",
]


# Global client instance
_client: BaseLLMClient | None = None


def get_ai_client(provider: str = "openai") -> BaseLLMClient:
    """Get an AI client instance.

    Factory function for creating AI clients. Returns a singleton
    instance for the default provider.

    Args:
        provider: AI provider name ("openai").

    Returns:
        AI client instance.

    Raises:
        ValueError: If provider is not supported.
        AuthenticationError: If API key is not configured.

    Example:
        >>> client = get_ai_client()
        >>> async with client:
        ...     response = await client.chat(request)
    """
    global _client  # noqa: PLW0603

    if provider == "openai":
        if _client is None:
            _client = OpenAIClient()
        return _client

    raise ValueError(f"Unsupported provider: {provider}")


async def close_ai_client() -> None:
    """Close the global AI client.

    Should be called on application shutdown.
    """
    global _client  # noqa: PLW0603
    if _client is not None:
        await _client.close()
        _client = None
