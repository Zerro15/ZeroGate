"""Эндпоинты авторизации."""
from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException, status

from backend.app.api import deps
from backend.app.core.config import settings
from backend.app.core.security import create_access_token
from backend.app.schemas.auth import LoginRequest, RegisterRequest, Token
from backend.app.schemas.user import UserCreate, UserOut
from backend.app.services.user_service import UserService

router = APIRouter()


def get_user_service(db=Depends(deps.get_db)) -> UserService:
    """Фабрика сервиса пользователей."""

    return UserService(db)


@router.post("/auth/register", response_model=UserOut, status_code=status.HTTP_201_CREATED)
def register_user(
    payload: RegisterRequest, user_service: UserService = Depends(get_user_service)
) -> UserOut:
    """Регистрирует нового пользователя.

    Если email уже занят, отдаём 400 с понятным сообщением.
    """

    existing = user_service.get_by_email(payload.email)
    if existing:
        raise HTTPException(status_code=400, detail="Пользователь с таким email уже существует")
    user_in = UserCreate(**payload.model_dump())
    return user_service.create(user_in=user_in)


@router.post("/auth/login", response_model=Token)
def login_for_access_token(
    payload: LoginRequest, user_service: UserService = Depends(get_user_service)
) -> Token:
    """Принимает логин/пароль и выдаёт access-токен при успехе."""

    user = user_service.authenticate(email=payload.email, password=payload.password)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Неверные креды")

    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    token = create_access_token(subject=str(user.id), expires_delta=access_token_expires)
    return Token(access_token=token)


@router.post("/auth/logout", response_model=Token)
def logout_stub() -> Token:
    """Заглушка для логаута: на клиенте просто забываем токен."""

    return Token(access_token="", token_type="bearer")
