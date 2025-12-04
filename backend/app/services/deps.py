"""FastAPI dependency utilities."""
import base64
import hashlib
import hmac
import json
import logging
import time
from typing import Union

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession

from backend.app.core.config import settings
from backend.app.db.session import get_session
from backend.app.models.user import User
from backend.app.services.auth import get_user_by_email

logger = logging.getLogger("zerrogate.deps")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")


def _b64url_decode(input_str: str) -> bytes:
    """Decode base64url-encoded string."""
    rem = len(input_str) % 4
    if rem:
        input_str += "=" * (4 - rem)
    return base64.urlsafe_b64decode(input_str.encode("utf-8"))


def jwt_decode_hs256(token: str, key: str) -> dict:
    """Minimal HS256 JWT decoder — verifies signature and expiration."""
    try:
        header_b64, payload_b64, sig_b64 = token.split(".")
    except ValueError:
        raise ValueError("Token structure invalid")

    signing_input = f"{header_b64}.{payload_b64}".encode("utf-8")
    expected_sig = hmac.new(key.encode("utf-8"), signing_input, hashlib.sha256).digest()

    try:
        sig = _b64url_decode(sig_b64)
    except Exception:
        raise ValueError("Invalid signature encoding")

    if not hmac.compare_digest(expected_sig, sig):
        raise ValueError("Signature verification failed")

    try:
        payload_bytes = _b64url_decode(payload_b64)
        payload = json.loads(payload_bytes.decode("utf-8"))
    except Exception:
        raise ValueError("Invalid payload")

    # Check expiration
    exp = payload.get("exp")
    if exp is None or not isinstance(exp, (int, float)):
        raise ValueError("exp claim missing or invalid")
    if int(time.time()) > int(exp):
        raise ValueError("Token has expired")

    return payload


async def get_current_user(
    token: str = Depends(oauth2_scheme), session: AsyncSession = Depends(get_session)
) -> User:
    """Extract and validate user from JWT token."""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt_decode_hs256(token, settings.JWT_SECRET_KEY)
        email: Union[str, None] = payload.get("sub")
        if email is None:
            raise credentials_exception
    except Exception as exc:
        logger.debug("JWT decode error: %s", exc)
        raise credentials_exception

    user = await get_user_by_email(session, email)
    if user is None:
        raise credentials_exception

    return user
