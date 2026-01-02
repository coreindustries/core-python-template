"""AI client configuration settings.

Settings for AI providers and client behavior.
"""

from functools import lru_cache

from pydantic import Field, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class AISettings(BaseSettings):
    """AI client configuration settings.

    Attributes:
        openai_api_key: OpenAI API key.
        openai_model: Default OpenAI model for chat.
        openai_embedding_model: OpenAI model for embeddings.
        openai_embedding_dimensions: Output dimensions for embeddings.
        openai_base_url: OpenAI API base URL (for proxies).
        timeout: Request timeout in seconds.
        max_retries: Maximum retry attempts.
    """

    model_config = SettingsConfigDict(
        env_file=".env",
        env_prefix="AI_",
        extra="ignore",
    )

    # OpenAI settings
    openai_api_key: SecretStr | None = None
    openai_model: str = "gpt-4o-mini"
    openai_embedding_model: str = "text-embedding-3-small"
    openai_embedding_dimensions: int = 1536
    openai_base_url: str | None = None

    # Client behavior
    timeout: float = Field(default=60.0, ge=1.0, le=600.0)
    max_retries: int = Field(default=3, ge=0, le=10)

    @property
    def has_openai(self) -> bool:
        """Check if OpenAI is configured.

        Returns:
            True if OpenAI API key is set.
        """
        return self.openai_api_key is not None


@lru_cache
def get_ai_settings() -> AISettings:
    """Get cached AI settings instance.

    Returns:
        AISettings singleton instance.
    """
    return AISettings()
