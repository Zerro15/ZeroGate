# backend/app/db/base.py

from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    """Базовый класс для всех ORM-моделей."""
    pass

# Важно: просто импортируем модели, чтобы они зарегистрировались в Base.metadata
from backend.app.models.user import User

__all__ = [
    "Base",
    "User",
]