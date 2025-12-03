"""User model for authentication and ownership."""
from sqlalchemy import Boolean, Column, Integer, String

from app.db.session import Base


class User(Base):
    __tablename__ = "users"

    id: int = Column(Integer, primary_key=True, index=True)
    email: str = Column(String, unique=True, index=True, nullable=False)
    hashed_password: str = Column(String, nullable=False)
    is_active: bool = Column(Boolean, default=True)
    is_admin: bool = Column(Boolean, default=False)

    # Комментарий: модель максимально простая для примера авторизации
