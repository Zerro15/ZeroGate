"""Database initialization and seeding."""
import logging
import os
from sqlalchemy.ext.asyncio import AsyncSession

from backend.app.core.config import settings
from backend.app.db.session import Base, engine
from backend.app.services.auth import ensure_admin_user

logger = logging.getLogger("zerrogate.db")


async def init_db() -> None:
    """Create tables and seed admin user if needed."""
    logger.info("CWD: %s", os.getcwd())
    logger.info("DATABASE_URL: %s", settings.DATABASE_URL)

    # Create all tables
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    # Create admin user if needed
    async with AsyncSession(engine) as session:
        await ensure_admin_user(session)
        logger.info("Database initialization complete")
