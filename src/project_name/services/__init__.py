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
# Example Service
# =============================================================================
# To create a service, inherit from BaseService and implement CRUD operations.
# Example pattern:
# - Import models: from project_name.models import User, UserCreate, UserUpdate
# - Import db: from project_name.db import get_db
# - Create service class inheriting from BaseService[User, UserCreate, UserUpdate]
# - Implement async methods: get_by_id, create, update, delete
