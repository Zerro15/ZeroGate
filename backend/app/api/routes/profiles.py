"""Роуты для управления профилями подключения."""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from backend.app.api import deps
from backend.app.models.user import User
from backend.app.schemas.profile import ProfileCreate, ProfileOut, ProfileUpdate
from backend.app.services.profile_service import ProfileService

router = APIRouter()


def get_profile_service(db: AsyncSession = Depends(deps.get_db)) -> ProfileService:
    """Фабрика сервиса профилей."""

    return ProfileService(db)


@router.get("/profiles", response_model=list[ProfileOut])
async def list_profiles(
    current_user: User = Depends(deps.get_current_active_user),
    service: ProfileService = Depends(get_profile_service),
):
    """Список профилей пользователя."""

    return await service.list_for_user(current_user.id)


@router.post("/profiles", response_model=ProfileOut, status_code=status.HTTP_201_CREATED)
async def create_profile(
    payload: ProfileCreate,
    current_user: User = Depends(deps.get_current_active_user),
    service: ProfileService = Depends(get_profile_service),
):
    """Создать профиль."""

    return await service.create(user_id=current_user.id, profile_in=payload)


@router.patch("/profiles/{profile_id}", response_model=ProfileOut)
async def update_profile(
    profile_id: int,
    payload: ProfileUpdate,
    current_user: User = Depends(deps.get_current_active_user),
    service: ProfileService = Depends(get_profile_service),
):
    """Обновить профиль."""

    profile = await service.get(profile_id, current_user.id)
    if not profile:
        raise HTTPException(status_code=404, detail="Профиль не найден")
    return await service.update(profile, payload)


@router.delete("/profiles/{profile_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_profile(
    profile_id: int,
    current_user: User = Depends(deps.get_current_active_user),
    service: ProfileService = Depends(get_profile_service),
):
    """Удалить профиль."""

    profile = await service.get(profile_id, current_user.id)
    if not profile:
        raise HTTPException(status_code=404, detail="Профиль не найден")
    await service.delete(profile)
    return None
