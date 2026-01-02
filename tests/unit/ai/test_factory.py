"""Tests for AI module factory functions."""

from unittest.mock import AsyncMock, patch

import pytest

import project_name.ai as ai_module
from project_name.ai import (
    close_ai_client,
    get_ai_client,
)
from project_name.ai.clients.openai import OpenAIClient


class TestGetAIClient:
    """Tests for get_ai_client factory function."""

    def setup_method(self) -> None:
        """Reset global client before each test."""
        ai_module._client = None

    def teardown_method(self) -> None:
        """Clean up global client after each test."""
        ai_module._client = None

    def test_get_ai_client_openai(self) -> None:
        """Test get_ai_client returns OpenAI client."""
        with patch.object(
            OpenAIClient,
            "__init__",
            lambda self, settings=None: setattr(self, "_settings", settings)
            or setattr(self, "_client", None)
            or setattr(self, "_tracker", None),
        ):
            client = get_ai_client("openai")
            assert client is not None

    def test_get_ai_client_returns_singleton(self) -> None:
        """Test get_ai_client returns same instance."""
        with patch.object(
            OpenAIClient,
            "__init__",
            lambda self, settings=None: setattr(self, "_settings", settings)
            or setattr(self, "_client", None)
            or setattr(self, "_tracker", None),
        ):
            client1 = get_ai_client("openai")
            client2 = get_ai_client("openai")
            assert client1 is client2

    def test_get_ai_client_unsupported_provider(self) -> None:
        """Test get_ai_client raises for unsupported provider."""
        with pytest.raises(ValueError, match="Unsupported provider"):
            get_ai_client("anthropic")


class TestCloseAIClient:
    """Tests for close_ai_client function."""

    def setup_method(self) -> None:
        """Reset global client before each test."""
        ai_module._client = None

    def teardown_method(self) -> None:
        """Clean up global client after each test."""
        ai_module._client = None

    @pytest.mark.asyncio
    async def test_close_ai_client_when_initialized(self) -> None:
        """Test close_ai_client when client exists."""
        # Create a mock client
        mock_client = AsyncMock()
        ai_module._client = mock_client

        await close_ai_client()

        mock_client.close.assert_called_once()
        assert ai_module._client is None

    @pytest.mark.asyncio
    async def test_close_ai_client_when_not_initialized(self) -> None:
        """Test close_ai_client when no client exists."""
        # Should not raise
        await close_ai_client()
        assert ai_module._client is None
