"""Connection profile model."""
from sqlalchemy import Boolean, Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from app.db.session import Base


class Profile(Base):
    __tablename__ = "profiles"

    id: int = Column(Integer, primary_key=True, index=True)
    name: str = Column(String, nullable=False)
    server: str = Column(String, nullable=False)
    port: int = Column(Integer, default=443)
    protocol: str = Column(String, default="generic")
    encryption: str = Column(String, default="AES-256 placeholder")
    is_active: bool = Column(Boolean, default=True)
    user_id: int = Column(Integer, ForeignKey("users.id"), nullable=False)

    user = relationship("User", backref="profiles")

    # Комментарий: модель хранит параметры профиля, но не сам туннель
