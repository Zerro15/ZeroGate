"""Database session and engine creation.

This module provides async SQLAlchemy session management for the backend.
Uses aiosqlite for SQLite with async support.
"""
from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import declarative_base

from backend.app.core.config import settings

# Базовый класс для всех ORM-моделей
Base = declarative_base()

# Асинхронный движок - используем DATABASE_URL из настроек
engine = create_async_engine(
    settings.DATABASE_URL,
    echo=settings.debug,
    future=True,
)

# Фабрика асинхронных сессий
AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    expire_on_commit=False,
    class_=AsyncSession,
)


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    """Dependency for FastAPI routes to provide DB session."""
    async with AsyncSessionLocal() as session:
        yield session


# Backwards-compatible aliases
get_db = get_session
async_session = get_session
