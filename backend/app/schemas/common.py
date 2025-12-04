"""Общие вспомогательные схемы."""
from pydantic import BaseModel


class Message(BaseModel):
    """Простая схема для текстового ответа."""

    detail: str
