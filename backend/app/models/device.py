"""Device model to track user devices."""
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.db.session import Base


class Device(Base):
    __tablename__ = "devices"

    id: int = Column(Integer, primary_key=True, index=True)
    name: str = Column(String, nullable=False)
    status: str = Column(String, default="offline")
    user_id: int = Column(Integer, ForeignKey("users.id"), nullable=False)

    user = relationship("User", backref="devices")

    # Комментарий: статус храним строкой для наглядности (online/offline)
