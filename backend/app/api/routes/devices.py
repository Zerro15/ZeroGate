"""Роуты для управления устройствами."""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from backend.app.api import deps
from backend.app.models.user import User
from backend.app.schemas.device import DeviceCreate, DeviceOut, DeviceUpdate
from backend.app.services.device_service import DeviceService

router = APIRouter()


def get_device_service(db: AsyncSession = Depends(deps.get_db)) -> DeviceService:
    """Фабрика сервиса устройств."""

    return DeviceService(db)


@router.get("/devices", response_model=list[DeviceOut])
async def list_devices(
    current_user: User = Depends(deps.get_current_active_user),
    service: DeviceService = Depends(get_device_service),
) -> list[DeviceOut]:
    """Список устройств текущего пользователя."""

    return await service.list_for_user(current_user.id)


@router.post("/devices", response_model=DeviceOut, status_code=status.HTTP_201_CREATED)
async def create_device(
    payload: DeviceCreate,
    current_user: User = Depends(deps.get_current_active_user),
    service: DeviceService = Depends(get_device_service),
) -> DeviceOut:
    """Создание нового устройства."""

    return await service.create(user_id=current_user.id, device_in=payload)


@router.get("/devices/{device_id}", response_model=DeviceOut)
async def get_device(
    device_id: int,
    current_user: User = Depends(deps.get_current_active_user),
    service: DeviceService = Depends(get_device_service),
) -> DeviceOut:
    """Возвращает одно устройство, если оно принадлежит текущему пользователю."""

    device = await service.get(device_id, current_user.id)
    if not device:
        raise HTTPException(status_code=404, detail="Устройство не найдено")
    return device


@router.patch("/devices/{device_id}", response_model=DeviceOut)
async def update_device(
    device_id: int,
    payload: DeviceUpdate,
    current_user: User = Depends(deps.get_current_active_user),
    service: DeviceService = Depends(get_device_service),
) -> DeviceOut:
    """Обновление имени или статуса устройства."""

    device = await service.get(device_id, current_user.id)
    if not device:
        raise HTTPException(status_code=404, detail="Устройство не найдено")
    return await service.update(device, payload)


@router.delete("/devices/{device_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_device(
    device_id: int,
    current_user: User = Depends(deps.get_current_active_user),
    service: DeviceService = Depends(get_device_service),
) -> None:
    """Удаление устройства."""

    device = await service.get(device_id, current_user.id)
    if not device:
        raise HTTPException(status_code=404, detail="Устройство не найдено")
    await service.delete(device)
    return None
