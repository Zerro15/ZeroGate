"""Device CRUD endpoints."""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_session
from app.models.device import Device
from app.schemas.device import DeviceCreate, DeviceRead, DeviceUpdate
from app.services.deps import get_current_user
from app.services.auth import require_active_user

router = APIRouter(prefix="/devices", tags=["devices"])


@router.get("/", response_model=list[DeviceRead])
async def list_devices(
    session: AsyncSession = Depends(get_session), current_user=Depends(get_current_user)
):
    await require_active_user(current_user)
    result = await session.execute(select(Device).where(Device.user_id == current_user.id))
    return result.scalars().all()


@router.post("/", response_model=DeviceRead, status_code=status.HTTP_201_CREATED)
async def create_device(
    payload: DeviceCreate,
    session: AsyncSession = Depends(get_session),
    current_user=Depends(get_current_user),
):
    await require_active_user(current_user)
    if payload.user_id != current_user.id and not current_user.is_admin:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Cannot assign to other user")
    device = Device(name=payload.name, status=payload.status, user_id=payload.user_id)
    session.add(device)
    await session.commit()
    await session.refresh(device)
    return device


@router.patch("/{device_id}", response_model=DeviceRead)
async def update_device(
    device_id: int,
    payload: DeviceUpdate,
    session: AsyncSession = Depends(get_session),
    current_user=Depends(get_current_user),
):
    await require_active_user(current_user)
    device = await session.get(Device, device_id)
    if not device or device.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Device not found")
    if payload.name is not None:
        device.name = payload.name
    if payload.status is not None:
        device.status = payload.status
    await session.commit()
    await session.refresh(device)
    return device


@router.delete("/{device_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_device(
    device_id: int,
    session: AsyncSession = Depends(get_session),
    current_user=Depends(get_current_user),
):
    await require_active_user(current_user)
    device = await session.get(Device, device_id)
    if not device or device.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Device not found")
    await session.delete(device)
    await session.commit()
    return None
