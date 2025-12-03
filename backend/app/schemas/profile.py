"""Schemas for connection profiles."""
from pydantic import BaseModel


class ProfileBase(BaseModel):
    name: str
    server: str
    port: int
    protocol: str
    encryption: str
    is_active: bool = True


class ProfileCreate(ProfileBase):
    user_id: int


class ProfileUpdate(BaseModel):
    name: str | None = None
    server: str | None = None
    port: int | None = None
    protocol: str | None = None
    encryption: str | None = None
    is_active: bool | None = None


class ProfileRead(ProfileBase):
    id: int
    user_id: int

    class Config:
        orm_mode = True
