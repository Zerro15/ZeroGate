"""Telemetry and log entries."""
from datetime import datetime

from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.db.session import Base


class LogEntry(Base):
    __tablename__ = "logs"

    id: int = Column(Integer, primary_key=True, index=True)
    device_id: int | None = Column(Integer, ForeignKey("devices.id"), nullable=True)
    level: str = Column(String, default="info")
    message: str = Column(String, nullable=False)
    created_at: datetime = Column(DateTime, default=datetime.utcnow)

    device = relationship("Device", backref="logs")

    # Комментарий: сохраняем простые события для демонстрации телеметрии
