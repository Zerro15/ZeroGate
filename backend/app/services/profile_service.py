"""Логика работы с профилями подключения."""
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.app.models.profile import ConnectionProfile
from backend.app.schemas.profile import ProfileCreate, ProfileUpdate


class ProfileService:
    """CRUD операции по профилям."""

    def __init__(self, db: AsyncSession):
        self.db = db

    async def list_for_user(self, user_id: int) -> list[ConnectionProfile]:
        """Список профилей конкретного пользователя."""

        result = await self.db.execute(
            select(ConnectionProfile).where(ConnectionProfile.user_id == user_id)
        )
        return list(result.scalars().all())

    async def get(self, profile_id: int, user_id: int) -> ConnectionProfile | None:
        """Получить профиль по id с проверкой владельца."""

        result = await self.db.execute(
            select(ConnectionProfile).where(
                ConnectionProfile.id == profile_id, ConnectionProfile.user_id == user_id
            )
        )
        return result.scalar_one_or_none()

    async def create(self, user_id: int, profile_in: ProfileCreate) -> ConnectionProfile:
        """Создать профиль."""

        db_profile = ConnectionProfile(user_id=user_id, **profile_in.model_dump())
        self.db.add(db_profile)
        await self.db.commit()
        await self.db.refresh(db_profile)
        return db_profile

    async def update(
        self, profile: ConnectionProfile, profile_in: ProfileUpdate
    ) -> ConnectionProfile:
        """Обновить поля профиля."""

        for field, value in profile_in.model_dump(exclude_none=True).items():
            setattr(profile, field, value)
        await self.db.commit()
        await self.db.refresh(profile)
        return profile

    async def delete(self, profile: ConnectionProfile) -> None:
        """Удалить профиль."""

        await self.db.delete(profile)
        await self.db.commit()
