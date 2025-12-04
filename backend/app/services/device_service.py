"""Логика работы с устройствами."""
from sqlalchemy.orm import Session

from backend.app.models.device import Device
from backend.app.schemas.device import DeviceCreate, DeviceUpdate


class DeviceService:
    """CRUD для устройств."""

    def __init__(self, db: Session):
        self.db = db

    def list_for_user(self, user_id: int) -> list[Device]:
        """Возвращает устройства пользователя."""

        return self.db.query(Device).filter(Device.owner_id == user_id).all()

    def get(self, device_id: int, user_id: int) -> Device | None:
        """Возвращает устройство по id, убеждаясь что владелец совпадает."""

        return (
            self.db.query(Device)
            .filter(Device.id == device_id, Device.owner_id == user_id)
            .first()
        )

    def create(self, user_id: int, device_in: DeviceCreate) -> Device:
        """Создаёт новое устройство."""

        db_device = Device(owner_id=user_id, name=device_in.name, status=device_in.status)
        self.db.add(db_device)
        self.db.commit()
        self.db.refresh(db_device)
        return db_device

    def update(self, device: Device, device_in: DeviceUpdate) -> Device:
        """Обновляет поля устройства."""

        if device_in.name is not None:
            device.name = device_in.name
        if device_in.status is not None:
            device.status = device_in.status
        self.db.commit()
        self.db.refresh(device)
        return device

    def delete(self, device: Device) -> None:
        """Удаляет устройство."""

        self.db.delete(device)
        self.db.commit()
