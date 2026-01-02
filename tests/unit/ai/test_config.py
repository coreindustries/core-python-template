"""Tests for AI configuration."""

import os
from unittest.mock import patch

from project_name.ai.config import AISettings


class TestAISettings:
    """Tests for AISettings."""

    def test_default_values(self) -> None:
        """Test default configuration values."""
        settings = AISettings()

        assert settings.openai_api_key is None
        assert settings.openai_model == "gpt-4o-mini"
        assert settings.openai_embedding_model == "text-embedding-3-small"
        assert settings.openai_embedding_dimensions == 1536
        assert settings.timeout == 60.0
        assert settings.max_retries == 3

    def test_has_openai_without_key(self) -> None:
        """Test has_openai without API key."""
        settings = AISettings()
        assert settings.has_openai is False

    def test_has_openai_with_key(self) -> None:
        """Test has_openai with API key."""
        with patch.dict(os.environ, {"AI_OPENAI_API_KEY": "sk-test"}):
            settings = AISettings()
            assert settings.has_openai is True

    def test_env_override(self) -> None:
        """Test environment variable override."""
        env_vars = {
            "AI_OPENAI_MODEL": "gpt-4o",
            "AI_TIMEOUT": "120.0",
            "AI_MAX_RETRIES": "5",
        }

        with patch.dict(os.environ, env_vars):
            settings = AISettings()
            assert settings.openai_model == "gpt-4o"
            assert settings.timeout == 120.0
            assert settings.max_retries == 5

    def test_api_key_is_secret(self) -> None:
        """Test API key is stored as secret."""
        with patch.dict(os.environ, {"AI_OPENAI_API_KEY": "sk-secret-key"}):
            settings = AISettings()

            # Should not be visible in string representation
            assert "sk-secret-key" not in str(settings.openai_api_key)

            # But accessible via get_secret_value
            assert settings.openai_api_key is not None
            assert settings.openai_api_key.get_secret_value() == "sk-secret-key"
