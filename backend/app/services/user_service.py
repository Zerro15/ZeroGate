"""Логика работы с пользователями."""
from datetime import datetime

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.app.core.security import get_password_hash, verify_password
from backend.app.models.user import User
from backend.app.schemas.user import UserCreate, UserUpdate


class UserService:
    """Сервис инкапсулирует CRUD для пользователей."""

    def __init__(self, session: AsyncSession):
        self.session = session

    async def get(self, user_id: int) -> User | None:
        """Возвращает пользователя по id или None."""

        result = await self.session.execute(select(User).where(User.id == user_id))
        return result.scalar_one_or_none()

    async def get_by_email(self, email: str) -> User | None:
        """Возвращает пользователя по email."""

        result = await self.session.execute(select(User).where(User.email == email))
        return result.scalar_one_or_none()

    async def create(self, user_in: UserCreate, is_admin: bool = False, is_active: bool = True) -> User:
        """Создаёт пользователя с хешированным паролем."""

        hashed_password = get_password_hash(user_in.password)
        db_user = User(
            email=user_in.email,
            full_name=user_in.full_name,
            hashed_password=hashed_password,
            is_active=is_active,
            is_admin=is_admin,
            created_at=datetime.utcnow(),
        )
        self.session.add(db_user)
        await self.session.commit()
        await self.session.refresh(db_user)
        return db_user

    async def update(self, db_user: User, user_in: UserUpdate) -> User:
        """Обновляет поля пользователя."""

        if user_in.email is not None:
            db_user.email = user_in.email
        if user_in.password is not None:
            db_user.hashed_password = get_password_hash(user_in.password)
        if user_in.is_active is not None:
            db_user.is_active = user_in.is_active
        if user_in.is_admin is not None:
            db_user.is_admin = user_in.is_admin
        if user_in.full_name is not None:
            db_user.full_name = user_in.full_name
        await self.session.commit()
        await self.session.refresh(db_user)
        return db_user

    async def authenticate(self, email: str, password: str) -> User | None:
        """Проверяет пару логин/пароль и возвращает пользователя или None."""

        user = await self.get_by_email(email)
        if not user:
            return None
        if not verify_password(password, user.hashed_password):
            return None
        return user
