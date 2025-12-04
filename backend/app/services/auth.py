"""Authentication and user helper utilities."""
from datetime import datetime, timedelta
from typing import Optional
import secrets

from fastapi import HTTPException, status
from jose import jwt
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.app.core.config import settings
from backend.app.core.security import get_password_hash, verify_password
from backend.app.models.user import User


async def authenticate_user(
    session: AsyncSession, email: str, password: str
) -> Optional[User]:
    """Validate user credentials and return user if valid."""

    query = select(User).where(User.email == email)
    result = await session.execute(query)
    user: Optional[User] = result.scalar_one_or_none()
    if not user or not verify_password(password, user.hashed_password):
        return None
    return user


def create_access_token(subject: str) -> str:
    """Generate JWT token for subject (user id)."""

    expire = datetime.utcnow() + timedelta(
        minutes=settings.JWT_ACCESS_TOKEN_EXPIRE_MINUTES
    )
    to_encode = {"sub": subject, "exp": expire, "jti": secrets.token_hex(8)}
    return jwt.encode(
        to_encode, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM
    )


async def get_user_by_email(session: AsyncSession, email: str) -> Optional[User]:
    """Fetch user by email."""

    result = await session.execute(select(User).where(User.email == email))
    return result.scalar_one_or_none()


async def ensure_admin_user(session: AsyncSession) -> None:
    """Create default admin if missing for demo purposes."""

    existing = await get_user_by_email(session, settings.FIRST_ADMIN_EMAIL)
    if existing:
        return
    admin = User(
        email=settings.FIRST_ADMIN_EMAIL,
        hashed_password=get_password_hash(settings.FIRST_ADMIN_PASSWORD),
        is_active=True,
        is_admin=True,
    )
    session.add(admin)
    await session.commit()


async def require_active_user(user: Optional[User]) -> User:
    """Ensure user exists and active."""

    if not user or not user.is_active:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Inactive user")
    return user
