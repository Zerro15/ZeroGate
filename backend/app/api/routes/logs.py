"""Роуты для работы с логами устройств."""
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from backend.app.api import deps
from backend.app.models.user import User
from backend.app.schemas.log import LogCreate, LogOut
from backend.app.services.log_service import LogService

router = APIRouter()


def get_log_service(db: AsyncSession = Depends(deps.get_db)) -> LogService:
    """Фабрика сервиса логов."""

    return LogService(db)


@router.get("/logs", response_model=list[LogOut])
async def list_logs(
    device_id: int | None = Query(default=None),
    current_user: User = Depends(deps.get_current_active_user),
    service: LogService = Depends(get_log_service),
) -> list[LogOut]:
    """Возвращает список логов по устройству или последние по всем."""

    if device_id is not None:
        return await service.for_device(current_user.id, device_id)
    return await service.recent(current_user.id)


@router.post("/logs", response_model=LogOut, status_code=status.HTTP_201_CREATED)
async def create_log(
    payload: LogCreate,
    current_user: User = Depends(deps.get_current_active_user),
    service: LogService = Depends(get_log_service),
) -> LogOut:
    """Создаёт лог, привязывая его к текущему пользователю."""

    if payload.device_id is None:
        raise HTTPException(status_code=400, detail="Нужно указать device_id")
    return await service.create(current_user.id, payload)
