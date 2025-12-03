"""Schemas for log entries."""
from datetime import datetime
from pydantic import BaseModel


class LogCreate(BaseModel):
    device_id: int | None = None
    level: str = "info"
    message: str


class LogRead(LogCreate):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True
