"""Tests for configuration module."""

import os
from unittest.mock import patch

import pytest

from project_name.config import Settings


class TestSettings:
    """Tests for Settings class."""

    def test_default_values(self) -> None:
        """Test default configuration values."""
        settings = Settings()

        assert settings.debug is False
        assert settings.log_level == "INFO"
        assert settings.environment == "development"
        assert settings.api_host == "0.0.0.0"  # noqa: S104  # Testing default value
        assert settings.api_port == 8000

    def test_is_development(self) -> None:
        """Test is_development property."""
        settings = Settings(environment="development")
        assert settings.is_development is True
        assert settings.is_production is False

    def test_is_production(self) -> None:
        """Test is_production property."""
        settings = Settings(environment="production")
        assert settings.is_production is True
        assert settings.is_development is False

    def test_env_override(self) -> None:
        """Test environment variable override."""
        with patch.dict(os.environ, {"DEBUG": "true", "LOG_LEVEL": "DEBUG"}):
            settings = Settings()
            assert settings.debug is True
            assert settings.log_level == "DEBUG"

    def test_invalid_log_level(self) -> None:
        """Test invalid log level raises error."""
        with pytest.raises(ValueError):
            Settings(log_level="INVALID")  # type: ignore[arg-type]
