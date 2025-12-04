"""Схемы для логов/телеметрии."""
from datetime import datetime

from pydantic import BaseModel, Field


class LogBase(BaseModel):
    """Базовое описание лог-сообщения."""

    message: str = Field(..., description="Короткое описание события")
    level: str = Field(default="info", description="Уровень важности: info/warn/error")
    device_id: int | None = Field(default=None, description="ID устройства, если есть связь")


class LogCreate(LogBase):
    """Данные для создания записи лога."""

    pass


class LogOut(LogBase):
    """Ответ наружу с техническими полями."""

    id: int
    user_id: int | None
    created_at: datetime

    class Config:
        from_attributes = True
