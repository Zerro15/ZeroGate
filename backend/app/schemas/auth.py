"""Схемы для авторизации."""
from pydantic import BaseModel, EmailStr


class Token(BaseModel):
    """Ответ с access-токеном."""

    access_token: str
    token_type: str = "bearer"


class TokenPayload(BaseModel):
    """Полезная нагрузка токена (что лежит внутри)."""

    sub: str | None = None


class LoginRequest(BaseModel):
    """Данные, которые передаёт пользователь при логине."""

    email: EmailStr
    password: str


class RegisterRequest(BaseModel):
    """Данные для регистрации нового пользователя."""

    email: EmailStr
    password: str
