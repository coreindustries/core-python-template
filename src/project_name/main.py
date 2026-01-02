"""FastAPI application entry point.

This module configures and creates the FastAPI application instance
with forensic security logging enabled.
"""

from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from project_name.api.routes import router
from project_name.config import settings
from project_name.logging import (
    AuditAction,
    SecurityEvent,
    configure_logging,
    get_audit_logger,
    get_logger,
)
from project_name.logging.middleware import RequestLoggingMiddleware


# Configure logging before anything else
configure_logging(
    level=settings.log_level,
    json_output=settings.log_json,
    log_file=settings.log_file,
    max_bytes=settings.log_file_max_bytes,
    backup_count=settings.log_file_backup_count,
    enable_masking=settings.log_mask_sensitive,
    environment=settings.environment,
)

logger = get_logger(__name__)
audit = get_audit_logger()


@asynccontextmanager
async def lifespan(_app: FastAPI) -> AsyncGenerator[None, None]:
    """Application lifespan manager.

    Handles startup and shutdown events for the application.
    Use this for database connections, cache initialization, etc.

    Args:
        app: FastAPI application instance.

    Yields:
        None during application runtime.
    """
    # Startup
    logger.info(
        "Application starting",
        extra={
            "event_type": "lifecycle",
            "environment": settings.environment,
            "debug": settings.debug,
        },
    )

    # Log startup as security event
    audit.log_event(
        SecurityEvent(
            action=AuditAction.SERVICE_START,
            actor_type="system",
            details=f"Application started in {settings.environment} mode",
            metadata={
                "environment": settings.environment,
                "debug": settings.debug,
                "version": "0.1.0",
            },
        )
    )

    # TODO: Initialize database connection
    # TODO: Initialize Redis connection if configured

    yield

    # Shutdown
    logger.info("Application shutting down", extra={"event_type": "lifecycle"})

    audit.log_event(
        SecurityEvent(
            action=AuditAction.SERVICE_STOP,
            actor_type="system",
            details="Application shutdown",
        )
    )

    # TODO: Close database connection
    # TODO: Close Redis connection


def create_app() -> FastAPI:
    """Create and configure the FastAPI application.

    Returns:
        Configured FastAPI application instance.
    """
    app = FastAPI(
        title="Project Name",  # TODO: Update project name
        description="A Python API built with FastAPI",
        version="0.1.0",
        docs_url="/docs" if settings.debug else None,
        redoc_url="/redoc" if settings.debug else None,
        lifespan=lifespan,
    )

    # Add request logging middleware (first, so it wraps everything)
    app.add_middleware(
        RequestLoggingMiddleware,
        exclude_paths=["/health", "/metrics", "/favicon.ico"],
        log_request_body=settings.log_request_body,
        log_response_body=settings.log_response_body,
    )

    # Configure CORS
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Include routers
    app.include_router(router)

    return app


# Application instance
app = create_app()
