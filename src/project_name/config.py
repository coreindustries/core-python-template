"""Application configuration using Pydantic Settings.

This module provides centralized configuration management with environment
variable support and type validation.
"""

from functools import lru_cache
from pathlib import Path
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
        log_json: Use JSON structured logging.
        log_file: Optional log file path.
        log_file_max_bytes: Max log file size before rotation.
        log_file_backup_count: Number of backup log files.
        log_mask_sensitive: Enable sensitive data masking.
        log_request_body: Log request bodies (use with caution).
        log_response_body: Log response bodies (use with caution).
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
    secret_key: str = "change-me-in-production"  # noqa: S105  # Default only, must be overridden

    # Logging - Forensic Security Logging
    log_json: bool = True  # Use JSON structured logging (recommended for production)
    log_file: Path | None = None  # Optional: logs/app.log
    log_file_max_bytes: int = 10_485_760  # 10 MB
    log_file_backup_count: int = 10
    log_mask_sensitive: bool = True  # Mask passwords, tokens, etc. in logs
    log_request_body: bool = False  # Log request bodies (PII risk - use with caution)
    log_response_body: bool = False  # Log response bodies (PII risk - use with caution)

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
