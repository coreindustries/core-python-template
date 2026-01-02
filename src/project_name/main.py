"""FastAPI application entry point.

This module configures and creates the FastAPI application instance
with forensic security logging and metrics collection.
"""

from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from project_name import __version__
from project_name.api.metrics import router as metrics_router
from project_name.api.routes import router
from project_name.config import settings
from project_name.db import close_db_client, get_db_client
from project_name.logging import (
    AuditAction,
    SecurityEvent,
    configure_logging,
    get_audit_logger,
    get_logger,
)
from project_name.logging.middleware import RequestLoggingMiddleware
from project_name.metrics import get_metrics_collector
from project_name.metrics.config import get_metrics_settings
from project_name.metrics.middleware import PrometheusMetricsMiddleware


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
                "version": __version__,
            },
        )
    )

    # Initialize database connection
    try:
        await get_db_client()
        logger.info("Database connection established")
    except Exception:
        logger.warning("Database connection failed - some features may be unavailable")

    # Initialize metrics
    metrics_settings = get_metrics_settings()
    if metrics_settings.enabled:
        collector = get_metrics_collector()
        collector.set_app_info(
            version=__version__,
            environment=settings.environment,
        )
        logger.info("Metrics collection enabled")

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

    # Close database connection
    await close_db_client()
    logger.info("Database connection closed")


def create_app() -> FastAPI:
    """Create and configure the FastAPI application.

    Returns:
        Configured FastAPI application instance.
    """
    app = FastAPI(
        title="Project Name",  # TODO: Update project name
        description="A Python API built with FastAPI",
        version=__version__,
        docs_url="/docs" if settings.debug else None,
        redoc_url="/redoc" if settings.debug else None,
        lifespan=lifespan,
    )

    # Add metrics middleware (first for accurate timing)
    metrics_settings = get_metrics_settings()
    if metrics_settings.enabled:
        app.add_middleware(
            PrometheusMetricsMiddleware,
            exclude_paths=["/health", "/metrics", "/favicon.ico"],
        )

    # Add request logging middleware
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
    app.include_router(metrics_router)

    return app


# Application instance
app = create_app()
