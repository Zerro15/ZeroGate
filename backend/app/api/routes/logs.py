"""Log endpoints for telemetry."""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_session
from app.models.log_entry import LogEntry
from app.models.device import Device
from app.schemas.log import LogCreate, LogRead
from app.services.deps import get_current_user
from app.services.auth import require_active_user

router = APIRouter(prefix="/logs", tags=["logs"])


@router.get("/recent", response_model=list[LogRead])
async def recent_logs(
    session: AsyncSession = Depends(get_session), current_user=Depends(get_current_user)
):
    await require_active_user(current_user)
    result = await session.execute(
        select(LogEntry).order_by(LogEntry.created_at.desc()).limit(50)
    )
    return result.scalars().all()


@router.get("/device/{device_id}", response_model=list[LogRead])
async def logs_by_device(
    device_id: int,
    session: AsyncSession = Depends(get_session),
    current_user=Depends(get_current_user),
):
    await require_active_user(current_user)
    device = await session.get(Device, device_id)
    if not device or device.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Device not found")
    result = await session.execute(
        select(LogEntry)
        .where(LogEntry.device_id == device_id)
        .order_by(LogEntry.created_at.desc())
    )
    return result.scalars().all()


@router.post("/", response_model=LogRead, status_code=status.HTTP_201_CREATED)
async def add_log(
    payload: LogCreate,
    session: AsyncSession = Depends(get_session),
    current_user=Depends(get_current_user),
):
    await require_active_user(current_user)
    log = LogEntry(device_id=payload.device_id, level=payload.level, message=payload.message)
    session.add(log)
    await session.commit()
    await session.refresh(log)
    return log
