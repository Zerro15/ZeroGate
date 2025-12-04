"""Общий Declarative Base для моделей SQLAlchemy."""
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    """Базовый класс для всех ORM-моделей.

    Здесь можно было бы включить общие поля, но для простоты оставляем пустым.
    """

    pass
