"""Логика работы с журналом событий."""
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.app.models.log_entry import LogEntry
from backend.app.schemas.log import LogCreate


class LogService:
    """CRUD/поиск логов."""

    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, user_id: int | None, log_in: LogCreate) -> LogEntry:
        """Создаёт запись лога."""

        db_log = LogEntry(**log_in.model_dump(), user_id=user_id)
        self.db.add(db_log)
        await self.db.commit()
        await self.db.refresh(db_log)
        return db_log

    async def recent(self, user_id: int, limit: int = 20) -> list[LogEntry]:
        """Последние события по устройствам пользователя."""

        result = await self.db.execute(
            select(LogEntry)
            .where(LogEntry.user_id == user_id)
            .order_by(LogEntry.created_at.desc())
            .limit(limit)
        )
        return list(result.scalars().all())

    async def for_device(
        self, user_id: int, device_id: int, limit: int = 50
    ) -> list[LogEntry]:
        """Логи по конкретному устройству."""

        result = await self.db.execute(
            select(LogEntry)
                .where(LogEntry.user_id == user_id, LogEntry.device_id == device_id)
                .order_by(LogEntry.created_at.desc())
                .limit(limit)
        )
        return list(result.scalars().all())
