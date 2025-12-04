"""Настройки приложения через pydantic-settings v2.

Все важные параметры собраны в одном месте, чтобы удобно было читать их
из окружения и использовать по всему проекту.
"""
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Базовые настройки проекта.

    Значения имеют разумные дефолты, но могут быть переопределены через
    переменные окружения или файл .env.
    """

    PROJECT_NAME: str = Field("ZeroGate", alias="PROJECT_NAME")
    VERSION: str = Field("0.1.0", alias="VERSION")
    API_V1_PREFIX: str = Field("/api", alias="API_V1_PREFIX")

    JWT_SECRET_KEY: str = Field("changeme-secret", alias="JWT_SECRET_KEY")
    JWT_ALGORITHM: str = Field("HS256", alias="JWT_ALGORITHM")
    JWT_ACCESS_TOKEN_EXPIRE_MINUTES: int = Field(
        60 * 24, alias="JWT_ACCESS_TOKEN_EXPIRE_MINUTES"
    )

    DATABASE_URL: str = Field(
        "sqlite+aiosqlite:///./zerrogate.db",
        alias="DATABASE_URL",
    )

    FIRST_ADMIN_EMAIL: str = Field(
        "admin@zerogate.local", alias="FIRST_ADMIN_EMAIL"
    )
    FIRST_ADMIN_PASSWORD: str = Field("admin", alias="FIRST_ADMIN_PASSWORD")
    SEED_ADMIN: bool = Field(True, alias="SEED_ADMIN")

    CREATE_DEMO_USER: bool = Field(False, alias="CREATE_DEMO_USER")
    DEMO_EMAIL: str = Field("demo@zerogate.local", alias="DEMO_EMAIL")
    DEMO_PASSWORD: str = Field("demo123", alias="DEMO_PASSWORD")

    DEBUG: bool = Field(False, alias="DEBUG")

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
        populate_by_name=True,
    )


settings = Settings()
