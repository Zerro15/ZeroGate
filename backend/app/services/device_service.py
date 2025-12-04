"""Логика работы с устройствами."""
from datetime import datetime

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.app.models.device import Device
from backend.app.schemas.device import DeviceCreate, DeviceUpdate


class DeviceService:
    """CRUD для устройств."""

    def __init__(self, db: AsyncSession):
        self.db = db

    async def list_for_user(self, user_id: int) -> list[Device]:
        """Возвращает устройства пользователя."""

        result = await self.db.execute(select(Device).where(Device.owner_id == user_id))
        return list(result.scalars().all())

    async def get(self, device_id: int, user_id: int) -> Device | None:
        """Возвращает устройство по id, убеждаясь что владелец совпадает."""

        result = await self.db.execute(
            select(Device).where(Device.id == device_id, Device.owner_id == user_id)
        )
        return result.scalar_one_or_none()

    async def create(self, user_id: int, device_in: DeviceCreate) -> Device:
        """Создаёт новое устройство."""

        db_device = Device(
            owner_id=user_id,
            name=device_in.name,
            status=device_in.status,
            device_type=device_in.device_type,
            created_at=datetime.utcnow(),
        )
        self.db.add(db_device)
        await self.db.commit()
        await self.db.refresh(db_device)
        return db_device

    async def update(self, device: Device, device_in: DeviceUpdate) -> Device:
        """Обновляет поля устройства."""

        if device_in.name is not None:
            device.name = device_in.name
        if device_in.status is not None:
            device.status = device_in.status
        if device_in.device_type is not None:
            device.device_type = device_in.device_type
        await self.db.commit()
        await self.db.refresh(device)
        return device

    async def delete(self, device: Device) -> None:
        """Удаляет устройство."""

        await self.db.delete(device)
        await self.db.commit()
