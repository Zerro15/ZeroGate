"""Status endpoint for health checks."""
from datetime import datetime

from fastapi import APIRouter

from app.core.config import settings
from app.schemas.auth import StatusResponse

router = APIRouter()


@router.get("/status", response_model=StatusResponse)
async def read_status() -> StatusResponse:
    """Return simple status payload."""
    # Комментарий: возвращаем время и версию, чтобы клиент видел жив ли сервер
    return StatusResponse(
        status="ok", version=settings.version, timestamp=datetime.utcnow().isoformat()
    )
