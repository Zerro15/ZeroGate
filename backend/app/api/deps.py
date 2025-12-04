"""Зависимости FastAPI для доступа к БД и текущему пользователю."""
from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.orm import Session

from backend.app.core.config import settings
from backend.app.db.session import get_db
from backend.app.models.user import User
from backend.app.schemas.auth import TokenPayload
from backend.app.services.user_service import UserService

# Схема авторизации через Bearer токен
oauth2_scheme = OAuth2PasswordBearer(tokenUrl=f"{settings.API_V1_PREFIX}/auth/login")

DbDep = Annotated[Session, Depends(get_db)]


def get_user_service(db: DbDep) -> UserService:
    """Возвращает сервис пользователей, чтобы не создавать его в каждом обработчике."""

    return UserService(db)


def get_current_user(
    db: DbDep, token: Annotated[str, Depends(oauth2_scheme)]
) -> User:
    """Извлекает пользователя из JWT токена.

    Если токен невалиден или пользователь не найден, бросаем 401.
    """

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Невалидный токен или пользователь не найден",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        token_data = TokenPayload(**payload)
    except JWTError as exc:  # type: ignore[arg-type]
        raise credentials_exception from exc
    if token_data.sub is None:
        raise credentials_exception

    user_service = get_user_service(db)
    user = user_service.get(int(token_data.sub))
    if user is None:
        raise credentials_exception
    return user


def get_current_active_user(current_user: Annotated[User, Depends(get_current_user)]) -> User:
    """Убеждаемся, что пользователь активен."""

    if not current_user.is_active:
        raise HTTPException(status_code=400, detail="Пользователь деактивирован")
    return current_user


def get_current_admin(current_user: Annotated[User, Depends(get_current_active_user)]) -> User:
    """Проверяем, что перед нами админ."""

    if not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Недостаточно прав")
    return current_user
