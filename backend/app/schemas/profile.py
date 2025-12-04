"""Схемы профилей подключений."""
from pydantic import BaseModel


class ProfileBase(BaseModel):
    """Основные поля профиля подключения."""

    name: str
    server: str
    port: int
    protocol_type: str
    encryption_info: str | None = None
    is_active: bool = False


class ProfileCreate(ProfileBase):
    """Схема создания профиля."""

    pass


class ProfileUpdate(BaseModel):
    """Схема обновления профиля."""

    name: str | None = None
    server: str | None = None
    port: int | None = None
    protocol_type: str | None = None
    encryption_info: str | None = None
    is_active: bool | None = None


class ProfileOut(ProfileBase):
    """Схема ответа наружу."""

    id: int
    user_id: int

    class Config:
        from_attributes = True
