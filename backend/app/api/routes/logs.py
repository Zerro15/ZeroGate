"""Роуты для чтения и записи логов."""
from fastapi import APIRouter, Depends, HTTPException

from backend.app.api import deps
from backend.app.models.user import User
from backend.app.schemas.log import LogCreate, LogOut
from backend.app.services.device_service import DeviceService
from backend.app.services.log_service import LogService

router = APIRouter()


def get_log_service(db=Depends(deps.get_db)) -> LogService:
    """Фабрика сервиса логов."""

    return LogService(db)


def get_device_service(db=Depends(deps.get_db)) -> DeviceService:
    """Фабрика сервиса устройств для проверки принадлежности."""

    return DeviceService(db)


@router.get("/logs", response_model=list[LogOut])
def read_logs(
    device_id: int | None = None,
    current_user: User = Depends(deps.get_current_active_user),
    service: LogService = Depends(get_log_service),
) -> list[LogOut]:
    """Возвращает последние события пользователя или конкретного устройства."""

    if device_id is not None:
        return service.for_device(user_id=current_user.id, device_id=device_id)
    return service.recent(user_id=current_user.id)


@router.post("/logs", response_model=LogOut, status_code=201)
def create_log(
    payload: LogCreate,
    current_user: User = Depends(deps.get_current_active_user),
    log_service: LogService = Depends(get_log_service),
    device_service: DeviceService = Depends(get_device_service),
) -> LogOut:
    """Создаёт запись лога, валидируя принадлежность устройства пользователю."""

    if payload.device_id is not None:
        device = device_service.get(device_id=payload.device_id, user_id=current_user.id)
        if not device:
            raise HTTPException(status_code=404, detail="Устройство не найдено или не принадлежит вам")
    return log_service.create(user_id=current_user.id, log_in=payload)
