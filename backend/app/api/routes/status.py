from datetime import datetime

from fastapi import APIRouter

# Создаём отдельный роутер для "технических" эндпоинтов статуса.
# Это удобно: логику можно группировать по модулям.
router = APIRouter(
    prefix="/api",    # общий префикс для всех маршрутов этого роутера
    tags=["status"],  # тег будет виден во /docs
)


@router.get("/status")
def get_status() -> dict:
    """Простой эндпоинт для проверки, что сервер работает.

    Здесь мы возвращаем базовую информацию о состоянии сервера:
    - название проекта;
    - статус (ok / error);
    - текущее серверное время.

    Этот эндпоинт удобно использовать:
    - в мобильном/desktop-клиенте;
    - в простой HTML-дашборде;
    - как healthcheck для мониторинга.
    """
    return {
        "project": "ZeroGate",
        "status": "ok",
        "time": datetime.utcnow().isoformat() + "Z",
    }
