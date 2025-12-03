"""Schemas for device representation."""
from pydantic import BaseModel


class DeviceBase(BaseModel):
    name: str
    status: str = "offline"


class DeviceCreate(DeviceBase):
    user_id: int


class DeviceUpdate(BaseModel):
    name: str | None = None
    status: str | None = None


class DeviceRead(DeviceBase):
    id: int
    user_id: int

    class Config:
        orm_mode = True
