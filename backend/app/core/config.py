# backend/app/core/config.py

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # версия сервиса для /api/status и Swagger
    VERSION: str = "0.1.0"

    # базовые настройки JWT
    JWT_SECRET_KEY: str = Field("changeme-secret", env="JWT_SECRET_KEY")
    JWT_ALGORITHM: str = Field("HS256", env="JWT_ALGORITHM")
    JWT_ACCESS_TOKEN_EXPIRE_MINUTES: int = Field(60 * 24, env="JWT_ACCESS_TOKEN_EXPIRE_MINUTES")

    # база (по умолчанию SQLite-файл)
    DATABASE_URL: str = Field(
        "sqlite+aiosqlite:///./zerrogate.db",
        env="DATABASE_URL",
    )

    # конфиг для pydantic-settings v2
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


settings = Settings()
