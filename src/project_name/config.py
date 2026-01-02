"""Application configuration using Pydantic Settings.

This module provides centralized configuration management with environment
variable support and type validation.
"""

from functools import lru_cache
from typing import Literal

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment variables.

    Attributes:
        database_url: PostgreSQL connection string.
        redis_url: Optional Redis connection string for caching.
        debug: Enable debug mode.
        log_level: Logging level.
        environment: Deployment environment.
        api_host: API server host.
        api_port: API server port.
        cors_origins: Allowed CORS origins.
        secret_key: Secret key for security features.
    """

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    # Database
    database_url: str = (
        "postgresql://postgres:postgres@localhost:5432/app"  # pragma: allowlist secret
    )

    # Redis optional
    redis_url: str | None = None

    # Application
    debug: bool = False
    log_level: Literal["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"] = "INFO"
    environment: Literal["development", "staging", "production"] = "development"

    # API
    api_host: str = "0.0.0.0"  # noqa: S104  # nosec B104  # Allow binding to all interfaces for server
    api_port: int = 8000
    cors_origins: list[str] = ["http://localhost:3000"]

    # Security
    secret_key: str = "change-me-in-production"

    @property
    def is_development(self) -> bool:
        """Check if running in development mode."""
        return self.environment == "development"

    @property
    def is_production(self) -> bool:
        """Check if running in production mode."""
        return self.environment == "production"


@lru_cache
def get_settings() -> Settings:
    """Get cached application settings.

    Returns:
        Application settings instance.
    """
    return Settings()


# Global settings instance for convenience
settings = get_settings()
