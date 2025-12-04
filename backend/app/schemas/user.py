"""Схемы пользователя."""
from datetime import datetime

from pydantic import BaseModel, EmailStr


class UserBase(BaseModel):
    """Базовые поля пользователя для чтения/записи."""

    email: EmailStr
    is_active: bool = True
    is_admin: bool = False


class UserCreate(BaseModel):
    """Схема для создания пользователя."""

    email: EmailStr
    password: str


class UserUpdate(BaseModel):
    """Схема обновления пользователя."""

    email: EmailStr | None = None
    password: str | None = None
    is_active: bool | None = None
    is_admin: bool | None = None


class UserOut(UserBase):
    """Ответ пользователю с публичными полями."""

    id: int
    created_at: datetime

    class Config:
        from_attributes = True
