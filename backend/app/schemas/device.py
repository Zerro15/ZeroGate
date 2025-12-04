"""Схемы устройств."""
from datetime import datetime

from pydantic import BaseModel


class DeviceBase(BaseModel):
    """Базовые поля устройства."""

    name: str
    device_type: str = "unknown"
    status: str = "offline"


class DeviceCreate(DeviceBase):
    """Поля, которые нужны при создании устройства."""

    pass


class DeviceUpdate(BaseModel):
    """Поля, которые можно менять у существующего устройства."""

    name: str | None = None
    device_type: str | None = None
    status: str | None = None


class DeviceOut(DeviceBase):
    """Ответ наружу с системными полями."""

    id: int
    owner_id: int
    created_at: datetime

    class Config:
        from_attributes = True
