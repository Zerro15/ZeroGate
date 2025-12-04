"""Authentication and user helper utilities."""
from typing import Optional
import secrets
import logging
import hmac
import hashlib
import base64
import json
import time
from fastapi import HTTPException, status
from passlib.context import CryptContext
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.app.core.config import settings
from backend.app.models.user import User

# Use argon2 as primary, with bcrypt as fallback for backward compatibility
# This avoids bcrypt version conflicts on some systems
try:
    pwd_context = CryptContext(schemes=["argon2", "bcrypt"], deprecated="auto")
except Exception:
    # Fallback: use only bcrypt if argon2 is not available
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Compare plain password with hash."""
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    """Hash password for storing. Bcrypt has 72-byte limit."""
    # Bcrypt can only hash passwords up to 72 bytes
    # Truncate if necessary to avoid ValueError
    password = password[:72] if len(password.encode('utf-8')) > 72 else password
    return pwd_context.hash(password)


async def authenticate_user(session: AsyncSession, email: str, password: str) -> Optional[User]:
    """Validate user credentials and return user if valid."""
    query = select(User).where(User.email == email)
    result = await session.execute(query)
    user: Optional[User] = result.scalar_one_or_none()
    # Use logger instead of printing to stdout
    logger = logging.getLogger("zerrogate.auth")
    if not user:
        logger.debug("User not found: %s", email)
        return None
    if not verify_password(password, user.hashed_password):
        logger.debug("Password mismatch for user: %s", email)
        return None
    logger.debug("User authenticated: %s", email)
    return user


def create_access_token(subject: str) -> str:
    """Generate JWT token for subject (user email)."""
    # Build a simple HS256 JWT without external dependencies to avoid
    # library/algorithm mismatches in different environments.
    expire = int(time.time()) + int(settings.JWT_ACCESS_TOKEN_EXPIRE_MINUTES * 60)
    header = {"alg": "HS256", "typ": "JWT"}
    payload = {"sub": subject, "exp": expire, "jti": secrets.token_hex(8)}

    def b64url_encode(data: bytes) -> str:
        return base64.urlsafe_b64encode(data).rstrip(b"=").decode("utf-8")

    header_b64 = b64url_encode(json.dumps(header, separators=(",", ":")).encode("utf-8"))
    payload_b64 = b64url_encode(json.dumps(payload, separators=(",", ":")).encode("utf-8"))
    signing_input = f"{header_b64}.{payload_b64}".encode("utf-8")
    key = settings.JWT_SECRET_KEY.encode("utf-8")
    signature = hmac.new(key, signing_input, hashlib.sha256).digest()
    signature_b64 = b64url_encode(signature)
    return f"{header_b64}.{payload_b64}.{signature_b64}"


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
