"""Функции безопасности: хеширование паролей и создание JWT."""
from datetime import datetime, timedelta, timezone
from typing import Any, Optional

from jose import jwt
from passlib.context import CryptContext

from .config import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Проверяет, совпадает ли введённый пароль с хешем.

    plain_password: str
        Пароль в открытом виде, который ввёл пользователь.
    hashed_password: str
        Хеш, который хранится в базе.
    """

    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    """Возвращает хеш пароля для хранения в базе.

    password: str
        Пароль, который нужно захешировать.
    """

    return pwd_context.hash(password)


def create_access_token(subject: str, expires_delta: Optional[timedelta] = None) -> str:
    """Создаёт JWT access token для заданного субъекта (обычно user id или email).

    subject: str
        Идентификатор пользователя, который будет положен в токен.
    expires_delta: Optional[timedelta]
        Сколько времени будет жить токен; если не указано, берём из настроек.
    """

    expire = datetime.now(timezone.utc) + (
        expires_delta or timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    to_encode: dict[str, Any] = {"sub": subject, "exp": expire}
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
