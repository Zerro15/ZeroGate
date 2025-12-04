"""Логика работы с профилями подключения."""
from sqlalchemy.orm import Session

from backend.app.models.profile import ConnectionProfile
from backend.app.schemas.profile import ProfileCreate, ProfileUpdate


class ProfileService:
    """CRUD операции по профилям."""

    def __init__(self, db: Session):
        self.db = db

    def list_for_user(self, user_id: int) -> list[ConnectionProfile]:
        """Список профилей конкретного пользователя."""

        return self.db.query(ConnectionProfile).filter(ConnectionProfile.user_id == user_id).all()

    def get(self, profile_id: int, user_id: int) -> ConnectionProfile | None:
        """Получить профиль по id с проверкой владельца."""

        return (
            self.db.query(ConnectionProfile)
            .filter(ConnectionProfile.id == profile_id, ConnectionProfile.user_id == user_id)
            .first()
        )

    def create(self, user_id: int, profile_in: ProfileCreate) -> ConnectionProfile:
        """Создать профиль."""

        db_profile = ConnectionProfile(user_id=user_id, **profile_in.model_dump())
        self.db.add(db_profile)
        self.db.commit()
        self.db.refresh(db_profile)
        return db_profile

    def update(self, profile: ConnectionProfile, profile_in: ProfileUpdate) -> ConnectionProfile:
        """Обновить поля профиля."""

        for field, value in profile_in.model_dump(exclude_none=True).items():
            setattr(profile, field, value)
        self.db.commit()
        self.db.refresh(profile)
        return profile

    def delete(self, profile: ConnectionProfile) -> None:
        """Удалить профиль."""

        self.db.delete(profile)
        self.db.commit()
