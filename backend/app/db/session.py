"""Создание асинхронного движка и фабрики сессий."""
from collections.abc import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from backend.app.core.config import settings

# Настраиваем асинхронный движок. Для SQLite нужен драйвер aiosqlite в URL.
engine = create_async_engine(settings.DATABASE_URL, echo=settings.DEBUG, future=True)

# Фабрика сессий, которую будем использовать в зависимостях FastAPI.
async_session_maker = async_sessionmaker(
    engine, expire_on_commit=False, class_=AsyncSession
)


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """Асинхронная зависимость FastAPI, отдаёт сессию и корректно закрывает её."""

    async with async_session_maker() as session:
        yield session


# Некоторые модули ожидают алиас get_session, оставляем для совместимости.
get_session = get_db
