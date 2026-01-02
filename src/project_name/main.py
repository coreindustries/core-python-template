"""FastAPI application entry point.

This module configures and creates the FastAPI application instance.
"""

from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from project_name.api.routes import router
from project_name.config import settings


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """Application lifespan manager.

    Handles startup and shutdown events for the application.
    Use this for database connections, cache initialization, etc.

    Args:
        app: FastAPI application instance.

    Yields:
        None during application runtime.
    """
    # Startup
    # TODO: Initialize database connection
    # TODO: Initialize Redis connection if configured
    yield
    # Shutdown
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
