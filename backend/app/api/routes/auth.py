"""Эндпоинты авторизации."""
from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from backend.app.api import deps
from backend.app.core.config import settings
from backend.app.core.security import create_access_token
from backend.app.schemas.auth import LoginRequest, RegisterRequest, Token
from backend.app.schemas.user import UserCreate, UserOut
from backend.app.services.user_service import UserService

router = APIRouter()


async def get_user_service(db: AsyncSession = Depends(deps.get_db)) -> UserService:
    """Фабрика сервиса пользователей."""

    return UserService(db)


@router.post("/auth/register", response_model=UserOut, status_code=status.HTTP_201_CREATED)
async def register_user(
    payload: RegisterRequest, user_service: UserService = Depends(get_user_service)
) -> UserOut:
    """Регистрирует нового пользователя.

    Если email уже занят, отдаём 400 с понятным сообщением.
    """

    existing = await user_service.get_by_email(payload.email)
    if existing:
        raise HTTPException(status_code=400, detail="Пользователь с таким email уже существует")
    user_in = UserCreate(**payload.model_dump())
    # Новые пользователи по умолчанию неактивны, чтобы админ мог их включить
    return await user_service.create(user_in=user_in, is_active=False)


@router.post("/auth/login", response_model=Token)
async def login_for_access_token(
    payload: LoginRequest, user_service: UserService = Depends(get_user_service)
) -> Token:
    """Принимает логин/пароль и выдаёт access-токен при успехе."""

    user = await user_service.authenticate(email=payload.email, password=payload.password)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Неверные креды")
    if not user.is_active:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Пользователь не активен")

    access_token_expires = timedelta(minutes=settings.JWT_ACCESS_TOKEN_EXPIRE_MINUTES)
    token = create_access_token(subject=str(user.id), expires_delta=access_token_expires)
    return Token(access_token=token)


@router.post("/auth/demo-login", response_model=Token)
async def demo_login(
    payload: LoginRequest, user_service: UserService = Depends(get_user_service)
) -> Token:
    """JSON-вариант логина, удобный для клиентов."""

    return await login_for_access_token(payload, user_service)


@router.post("/auth/logout", response_model=Token)
async def logout_stub() -> Token:
    """Заглушка для логаута: на клиенте просто забываем токен."""

    return Token(access_token="", token_type="bearer")


@router.get("/auth/me", response_model=UserOut)
async def read_me(current_user=Depends(deps.get_current_active_user)) -> UserOut:
    """Возвращает данные текущего пользователя."""

    return current_user
