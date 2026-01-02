"""Base AI client interface.

Abstract base class for LLM provider implementations.
"""

from abc import ABC, abstractmethod
from collections.abc import AsyncIterator
from typing import Any

from project_name.ai.models import (
    ChatRequest,
    ChatResponse,
    EmbeddingRequest,
    EmbeddingResponse,
)


class BaseLLMClient(ABC):
    """Abstract base class for LLM provider clients.

    All LLM provider implementations must inherit from this class
    and implement the required async methods.

    Example:
        >>> class MyClient(BaseLLMClient):
        ...     async def chat(self, request: ChatRequest) -> ChatResponse:
        ...         # Implementation here
        ...         pass
    """

    @property
    @abstractmethod
    def provider(self) -> str:
        """Get the provider name.

        Returns:
            Provider name string.
        """
        ...

    @abstractmethod
    async def chat(self, request: ChatRequest) -> ChatResponse:
        """Send a chat completion request.

        Args:
            request: Chat completion request with messages and parameters.

        Returns:
            Chat completion response with generated content.

        Raises:
            AIClientError: If the request fails.
        """
        ...

    @abstractmethod
    async def chat_stream(
        self,
        request: ChatRequest,
    ) -> AsyncIterator[str]:
        """Stream a chat completion response.

        Args:
            request: Chat completion request with messages and parameters.

        Yields:
            Chunks of generated content as they arrive.

        Raises:
            AIClientError: If the request fails.
        """
        ...
        yield ""  # pragma: no cover

    @abstractmethod
    async def embed(self, request: EmbeddingRequest) -> EmbeddingResponse:
        """Generate embeddings for text.

        Args:
            request: Embedding request with texts to embed.

        Returns:
            Embedding response with vectors.

        Raises:
            AIClientError: If the request fails.
        """
        ...

    @abstractmethod
    async def close(self) -> None:
        """Close the client and release resources.

        Should be called when the client is no longer needed.
        """
        ...

    async def __aenter__(self) -> "BaseLLMClient":
        """Async context manager entry.

        Returns:
            The client instance.
        """
        return self

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: Any,
    ) -> None:
        """Async context manager exit.

        Args:
            exc_type: Exception type if raised.
            exc_val: Exception value if raised.
            exc_tb: Exception traceback if raised.
        """
        await self.close()
