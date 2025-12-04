"""Authentication endpoints."""
from __future__ import annotations


from fastapi import APIRouter, Depends, HTTPException, status
import logging
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from backend.app.db.session import get_session
from backend.app.models.user import User
from backend.app.schemas.auth import Token
from backend.app.schemas.user import UserLogin, UserRead
from backend.app.services import auth as auth_service
from backend.app.services.deps import get_current_user

router = APIRouter(prefix="/api/auth", tags=["auth"])


@router.post("/login", response_model=Token)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    session: AsyncSession = Depends(get_session),
) -> Token:
    """Login endpoint that returns JWT token."""
    logger = logging.getLogger("zerrogate.api.auth")
    try:
        user = await auth_service.authenticate_user(session, form_data.username, form_data.password)
        if not user:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect credentials")
        token = auth_service.create_access_token(user.email)
        return Token(access_token=token)
    except HTTPException:
        raise
    except Exception as exc:  # pragma: no cover - debugging helper
        logger.exception("Unexpected error in login endpoint")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")


@router.post("/demo-login", response_model=Token)
async def demo_login(payload: UserLogin, session: AsyncSession = Depends(get_session)) -> Token:
    """Alternative login for JSON payloads (удобно для мобильного клиента)."""
    logger = logging.getLogger("zerrogate.api.auth")
    try:
        user = await auth_service.authenticate_user(session, payload.email, payload.password)
        if not user:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect credentials")
        token = auth_service.create_access_token(user.email)
        return Token(access_token=token)
    except HTTPException:
        raise
    except Exception:
        logger.exception("Unexpected error in demo-login endpoint")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")


@router.get("/me", response_model=UserRead)
async def get_me(current_user: User = Depends(get_current_user)) -> UserRead:
    """Return info about current user (пока без ролей в ответе)."""
    await auth_service.require_active_user(current_user)
    return current_user
