"""Роут для проверки статуса API."""
from datetime import datetime, timezone

from fastapi import APIRouter
from fastapi.responses import JSONResponse

from backend.app.core.config import settings

router = APIRouter()


@router.get("/status", response_class=JSONResponse)
def read_status() -> dict[str, object]:
    """Возвращает базовый статус сервера."""

    return {
        "project": settings.PROJECT_NAME,
        "version": settings.VERSION,
        "status": "ok",
        "time": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
    }
