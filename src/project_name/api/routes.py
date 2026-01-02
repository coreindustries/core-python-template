"""API route definitions.

This module contains the main API routes for the application.
"""

from fastapi import APIRouter

from project_name import __version__


router = APIRouter()


@router.get("/health")
async def health_check() -> dict[str, str]:
    """Health check endpoint.

    Returns:
        Health status of the application.
    """
    return {"status": "healthy", "version": __version__}


@router.get("/")
async def root() -> dict[str, str]:
    """Root endpoint.

    Returns:
        Welcome message.
    """
    return {"message": "Welcome to Project Name API"}  # TODO: Update name


# =============================================================================
# Example CRUD routes
# =============================================================================
# To add CRUD routes, create new routers in separate files and include them.
# Use router.include_router() with prefix and tags parameters.
