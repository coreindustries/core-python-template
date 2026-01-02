"""OpenAI client implementation.

Client for OpenAI API chat completions and embeddings.
"""

import time
from collections.abc import AsyncIterator
from typing import Any

from project_name.ai.base import BaseLLMClient
from project_name.ai.config import AISettings, get_ai_settings
from project_name.ai.exceptions import (
    AIClientError,
    AuthenticationError,
    ContextLengthExceededError,
    InvalidRequestError,
    RateLimitError,
)
from project_name.ai.models import (
    ChatRequest,
    ChatResponse,
    EmbeddingRequest,
    EmbeddingResponse,
    TokenUsage,
)
from project_name.ai.tracking import TokenUsageRecord, get_token_tracker
from project_name.logging import get_logger


logger = get_logger(__name__)


class OpenAIClient(BaseLLMClient):
    """OpenAI API client.

    Implements chat completions and embeddings using the OpenAI API.

    Example:
        >>> async with OpenAIClient() as client:
        ...     response = await client.chat(ChatRequest(
        ...         messages=[ChatMessage.user("Hello!")],
        ...     ))
        ...     print(response.content)
    """

    def __init__(self, settings: AISettings | None = None) -> None:
        """Initialize OpenAI client.

        Args:
            settings: AI settings. Uses global settings if not provided.

        Raises:
            AuthenticationError: If API key is not configured.
        """
        self._settings = settings or get_ai_settings()
        if not self._settings.has_openai:
            raise AuthenticationError(
                "OpenAI API key not configured",
                provider="openai",
            )

        self._client: Any = None
        self._tracker = get_token_tracker()

    @property
    def provider(self) -> str:
        """Get the provider name.

        Returns:
            Provider name string.
        """
        return "openai"

    def _get_client(self) -> Any:
        """Get or create the OpenAI client.

        Returns:
            OpenAI client instance.
        """
        if self._client is None:
            try:
                from openai import AsyncOpenAI  # noqa: PLC0415
            except ImportError as e:
                raise AIClientError(
                    "openai package not installed. Install with: uv add openai",
                    provider="openai",
                ) from e

            api_key = self._settings.openai_api_key
            self._client = AsyncOpenAI(
                api_key=api_key.get_secret_value() if api_key else None,
                base_url=self._settings.openai_base_url,
                timeout=self._settings.timeout,
                max_retries=self._settings.max_retries,
            )
        return self._client

    async def chat(self, request: ChatRequest) -> ChatResponse:
        """Send a chat completion request.

        Args:
            request: Chat completion request with messages and parameters.

        Returns:
            Chat completion response with generated content.

        Raises:
            AIClientError: If the request fails.
        """
        client = self._get_client()
        model = request.model or self._settings.openai_model

        messages = [
            {"role": msg.role, "content": msg.content}
            for msg in request.messages
        ]

        start_time = time.perf_counter()

        try:
            response = await client.chat.completions.create(
                model=model,
                messages=messages,
                temperature=request.temperature,
                max_tokens=request.max_tokens,
                top_p=request.top_p,
                stop=request.stop,
                stream=False,
            )
        except Exception as e:
            self._handle_error(e)

        latency_ms = (time.perf_counter() - start_time) * 1000

        # Extract response data
        choice = response.choices[0]
        usage = TokenUsage(
            prompt_tokens=response.usage.prompt_tokens if response.usage else 0,
            completion_tokens=(
                response.usage.completion_tokens if response.usage else 0
            ),
            total_tokens=response.usage.total_tokens if response.usage else 0,
        )

        # Track token usage
        self._tracker.record(
            TokenUsageRecord(
                prompt_tokens=usage.prompt_tokens,
                completion_tokens=usage.completion_tokens,
                total_tokens=usage.total_tokens,
                model=model,
                provider=self.provider,
                metadata={"latency_ms": latency_ms},
            )
        )

        logger.debug(
            "Chat completion successful",
            extra={
                "model": model,
                "latency_ms": latency_ms,
                "tokens": usage.total_tokens,
            },
        )

        return ChatResponse(
            id=response.id,
            content=choice.message.content or "",
            model=response.model,
            usage=usage,
            finish_reason=choice.finish_reason,
        )

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
        client = self._get_client()
        model = request.model or self._settings.openai_model

        messages = [
            {"role": msg.role, "content": msg.content}
            for msg in request.messages
        ]

        try:
            stream = await client.chat.completions.create(
                model=model,
                messages=messages,
                temperature=request.temperature,
                max_tokens=request.max_tokens,
                top_p=request.top_p,
                stop=request.stop,
                stream=True,
            )

            async for chunk in stream:
                if chunk.choices and chunk.choices[0].delta.content:
                    yield chunk.choices[0].delta.content

        except Exception as e:
            self._handle_error(e)

    async def embed(self, request: EmbeddingRequest) -> EmbeddingResponse:
        """Generate embeddings for text.

        Args:
            request: Embedding request with texts to embed.

        Returns:
            Embedding response with vectors.

        Raises:
            AIClientError: If the request fails.
        """
        client = self._get_client()
        model = request.model or self._settings.openai_embedding_model
        dimensions = request.dimensions or self._settings.openai_embedding_dimensions

        start_time = time.perf_counter()

        try:
            response = await client.embeddings.create(
                model=model,
                input=request.texts,
                dimensions=dimensions,
            )
        except Exception as e:
            self._handle_error(e)

        latency_ms = (time.perf_counter() - start_time) * 1000

        # Extract embeddings
        embeddings = [item.embedding for item in response.data]
        usage = TokenUsage(
            prompt_tokens=response.usage.prompt_tokens if response.usage else 0,
            total_tokens=response.usage.total_tokens if response.usage else 0,
        )

        # Track token usage
        self._tracker.record(
            TokenUsageRecord(
                prompt_tokens=usage.prompt_tokens,
                total_tokens=usage.total_tokens,
                model=model,
                provider=self.provider,
                metadata={"latency_ms": latency_ms, "text_count": len(request.texts)},
            )
        )

        logger.debug(
            "Embedding generation successful",
            extra={
                "model": model,
                "latency_ms": latency_ms,
                "text_count": len(request.texts),
                "dimensions": dimensions,
            },
        )

        return EmbeddingResponse(
            embeddings=embeddings,
            model=response.model,
            usage=usage,
        )

    async def close(self) -> None:
        """Close the client and release resources."""
        if self._client is not None:
            await self._client.close()
            self._client = None

    def _handle_error(self, error: Exception) -> None:
        """Handle OpenAI API errors.

        Args:
            error: Exception to handle.

        Raises:
            AIClientError: Appropriate subclass based on error type.
        """
        error_str = str(error).lower()

        if "rate limit" in error_str or "429" in error_str:
            raise RateLimitError(
                str(error),
                provider=self.provider,
            ) from error

        if "authentication" in error_str or "401" in error_str:
            raise AuthenticationError(
                str(error),
                provider=self.provider,
            ) from error

        if "context length" in error_str or "maximum context" in error_str:
            raise ContextLengthExceededError(
                str(error),
                provider=self.provider,
            ) from error

        if "invalid" in error_str or "400" in error_str:
            raise InvalidRequestError(
                str(error),
                provider=self.provider,
            ) from error

        raise AIClientError(
            str(error),
            provider=self.provider,
        ) from error
