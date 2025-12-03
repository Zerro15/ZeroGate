"""Database session and engine creation."""
from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import declarative_base

from app.core.config import settings


Base = declarative_base()
engine = create_async_engine(settings.database_url, echo=settings.debug, future=True)
SessionLocal = async_sessionmaker(bind=engine, expire_on_commit=False, class_=AsyncSession)


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    """Dependency for FastAPI routes to provide DB session."""
    async with SessionLocal() as session:
        # Здесь мы открываем новую сессию и отдаем её в запрос
        yield session
        # После завершения запроса сессия будет автоматически закрыта
