"""Authentication endpoints."""
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from backend.app.db.session import get_session
from backend.app.schemas.auth import Token
from backend.app.schemas.user import UserLogin, UserRead
from backend.app.services import auth as auth_service
from backend.app.services.deps import get_current_user

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/login", response_model=Token)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    session: AsyncSession = Depends(get_session),
) -> Token:
    """Login endpoint that returns JWT token."""
    user = await auth_service.authenticate_user(session, form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect credentials")
    token = auth_service.create_access_token(user.email)
    return Token(access_token=token)


@router.post("/demo-login", response_model=Token)
async def demo_login(payload: UserLogin, session: AsyncSession = Depends(get_session)) -> Token:
    """Alternative login for JSON payloads (удобно для мобильного клиента)."""
    user = await auth_service.authenticate_user(session, payload.email, payload.password)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect credentials")
    token = auth_service.create_access_token(user.email)
    return Token(access_token=token)


@router.get("/me", response_model=UserRead)
async def get_me(current_user=Depends(get_current_user)):
    """Return info about current user (пока без ролей в ответе)."""
    await auth_service.require_active_user(current_user)
    return current_user
