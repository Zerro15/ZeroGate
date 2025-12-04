"""Authentication and user helper utilities."""
from datetime import datetime, timedelta
from typing import Optional
import secrets

from fastapi import HTTPException, status
from jose import jwt
from passlib.context import CryptContext
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.models.user import User

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Compare plain password with hash."""
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    """Hash password for storing."""
    return pwd_context.hash(password)


async def authenticate_user(session: AsyncSession, email: str, password: str) -> Optional[User]:
    """Validate user credentials and return user if valid."""
    query = select(User).where(User.email == email)
    result = await session.execute(query)
    user: Optional[User] = result.scalar_one_or_none()
    if not user or not verify_password(password, user.hashed_password):
        return None
    return user


def create_access_token(subject: str) -> str:
    """Generate JWT token for subject (user email)."""
    expire = datetime.utcnow() + timedelta(minutes=settings.access_token_expire_minutes)
    to_encode = {"sub": subject, "exp": expire, "jti": secrets.token_hex(8)}
    return jwt.encode(to_encode, settings.secret_key, algorithm="HS256")


async def get_user_by_email(session: AsyncSession, email: str) -> Optional[User]:
    """Fetch user by email."""
    result = await session.execute(select(User).where(User.email == email))
    return result.scalar_one_or_none()


async def ensure_admin_user(session: AsyncSession) -> None:
    """Create default admin if missing for demo purposes."""
    existing = await get_user_by_email(session, settings.admin_email)
    if existing:
        return
    admin = User(
        email=settings.admin_email,
        hashed_password=get_password_hash(settings.admin_password),
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
