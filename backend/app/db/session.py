"""Создание асинхронного движка и фабрики сессий."""
from collections.abc import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from backend.app.core.config import settings

# Настраиваем асинхронный движок. Для SQLite нужен драйвер aiosqlite в URL.
engine = create_async_engine(settings.DATABASE_URL, echo=settings.DEBUG, future=True)

# Фабрика сессий, которую будем использовать в зависимостях FastAPI.
async_session_maker = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    """Асинхронная зависимость FastAPI, отдаёт сессию и корректно закрывает её."""

    async with async_session_maker() as session:
        yield session
