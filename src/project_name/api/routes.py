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
# Example CRUD routes - uncomment and modify as needed
# =============================================================================

# from fastapi import HTTPException, status
# from project_name.models.user import User, UserCreate
# from project_name.services.user import UserService

# user_router = APIRouter(prefix="/users", tags=["users"])

# @user_router.post("/", response_model=User, status_code=status.HTTP_201_CREATED)
# async def create_user(user_data: UserCreate) -> User:
#     """Create a new user."""
#     service = UserService()
#     return await service.create(user_data)

# @user_router.get("/{user_id}", response_model=User)
# async def get_user(user_id: str) -> User:
#     """Get a user by ID."""
#     service = UserService()
#     user = await service.get_by_id(user_id)
#     if not user:
#         raise HTTPException(status_code=404, detail="User not found")
#     return user

# router.include_router(user_router)
