"""Business logic services.

This module contains service classes that implement business logic
and coordinate between the API layer and data access layer.
"""

from abc import ABC, abstractmethod
from typing import Generic, TypeVar

from pydantic import BaseModel

# Type variables for generic service
T = TypeVar("T")  # Entity type
CreateT = TypeVar("CreateT", bound=BaseModel)  # Create DTO type
UpdateT = TypeVar("UpdateT", bound=BaseModel)  # Update DTO type


class BaseService(ABC, Generic[T, CreateT, UpdateT]):
    """Abstract base service with common CRUD operations.

    Inherit from this class to implement domain-specific services.
    """

    @abstractmethod
    async def get_by_id(self, entity_id: str) -> T | None:
        """Get an entity by ID.

        Args:
            entity_id: Unique identifier.

        Returns:
            Entity if found, None otherwise.
        """
        ...

    @abstractmethod
    async def create(self, data: CreateT) -> T:
        """Create a new entity.

        Args:
            data: Data for creating the entity.

        Returns:
            Created entity.
        """
        ...

    @abstractmethod
    async def update(self, entity_id: str, data: UpdateT) -> T | None:
        """Update an existing entity.

        Args:
            entity_id: Unique identifier.
            data: Data for updating the entity.

        Returns:
            Updated entity if found, None otherwise.
        """
        ...

    @abstractmethod
    async def delete(self, entity_id: str) -> bool:
        """Delete an entity.

        Args:
            entity_id: Unique identifier.

        Returns:
            True if deleted, False if not found.
        """
        ...


# =============================================================================
# Example Service - uncomment and modify as needed
# =============================================================================

# from project_name.models import User, UserCreate, UserUpdate
# from project_name.db import get_db

# class UserService(BaseService[User, UserCreate, UserUpdate]):
#     """Service for user operations."""

#     async def get_by_id(self, entity_id: str) -> User | None:
#         async with get_db() as db:
#             user = await db.user.find_unique(where={"id": entity_id})
#             return User.model_validate(user) if user else None

#     async def create(self, data: UserCreate) -> User:
#         async with get_db() as db:
#             user = await db.user.create(data=data.model_dump())
#             return User.model_validate(user)

#     async def update(self, entity_id: str, data: UserUpdate) -> User | None:
#         async with get_db() as db:
#             update_data = data.model_dump(exclude_unset=True)
#             if not update_data:
#                 return await self.get_by_id(entity_id)
#             user = await db.user.update(
#                 where={"id": entity_id},
#                 data=update_data,
#             )
#             return User.model_validate(user) if user else None

#     async def delete(self, entity_id: str) -> bool:
#         async with get_db() as db:
#             try:
#                 await db.user.delete(where={"id": entity_id})
#                 return True
#             except Exception:
#                 return False
