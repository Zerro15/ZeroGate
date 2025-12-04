from datetime import datetime

from fastapi import APIRouter

router = APIRouter(
    prefix="/api",
    tags=["status"],
)


@router.get("/status")
def get_status() -> dict:
    """Простой эндпоинт для проверки, что сервер работает.

    Возвращает:
    - название проекта;
    - статус;
    - версию backend;
    - текущее серверное время (UTC).
    """
    return {
        "project": "ZeroGate",
        "status": "ok",
        "version": "0.1.0",  # важно: это поле нужно тесту
        "time": datetime.utcnow().isoformat() + "Z",
    }