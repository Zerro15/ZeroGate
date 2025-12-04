"""ORM-модель события (логов)."""
from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, Integer, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.app.db.base import Base


class LogEntry(Base):
    """Запись журнала: что произошло и когда."""

    __tablename__ = "log_entries"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    device_id: Mapped[int | None] = mapped_column(
        ForeignKey("devices.id", ondelete="SET NULL"), nullable=True
    )
    user_id: Mapped[int | None] = mapped_column(
        ForeignKey("users.id", ondelete="SET NULL"), nullable=True
    )
    message: Mapped[str] = mapped_column(String, nullable=False)
    level: Mapped[str] = mapped_column(String, default="info")
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )

    device = relationship("Device", back_populates="logs")
    user = relationship("User", back_populates="logs")
