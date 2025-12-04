"""Schemas for user-related DTOs."""
from pydantic import BaseModel, Field


class UserRead(BaseModel):
    """User response DTO (used for /api/auth/me)."""

    id: int
    email: str
    is_active: bool = True
    is_admin: bool = False

    model_config = {"from_attributes": True}


class UserLogin(BaseModel):
    """User login request DTO."""

    email: str = Field(..., min_length=1)
    password: str = Field(..., min_length=1)
