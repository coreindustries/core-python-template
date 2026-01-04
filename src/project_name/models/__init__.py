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
