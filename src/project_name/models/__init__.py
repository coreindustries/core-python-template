"""Data models using Pydantic.

This module contains Pydantic models for request/response validation
and data transfer objects.
"""

from pydantic import BaseModel, ConfigDict


class BaseSchema(BaseModel):
    """Base schema with common configuration.

    All API schemas should inherit from this class.
    """

    model_config = ConfigDict(
        from_attributes=True,  # Enable ORM mode
        str_strip_whitespace=True,  # Strip whitespace from strings
        validate_assignment=True,  # Validate on attribute assignment
    )


# =============================================================================
# Example Models - uncomment and modify as needed
# =============================================================================

# from datetime import datetime
# from pydantic import EmailStr, Field

# class UserBase(BaseSchema):
#     """Base user schema with common fields."""
#     email: EmailStr
#     name: str = Field(min_length=1, max_length=100)

# class UserCreate(UserBase):
#     """Schema for creating a new user."""
#     pass

# class UserUpdate(BaseSchema):
#     """Schema for updating a user."""
#     email: EmailStr | None = None
#     name: str | None = Field(default=None, min_length=1, max_length=100)

# class User(UserBase):
#     """Schema for user responses."""
#     id: str
#     created_at: datetime
#     updated_at: datetime
