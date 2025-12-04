"""Роуты для управления профилями подключений."""
from fastapi import APIRouter, Depends, HTTPException, status

from backend.app.api import deps
from backend.app.models.user import User
from backend.app.schemas.profile import ProfileCreate, ProfileOut, ProfileUpdate
from backend.app.services.profile_service import ProfileService

router = APIRouter()


def get_profile_service(db=Depends(deps.get_db)) -> ProfileService:
    """Фабрика сервиса профилей."""

    return ProfileService(db)


@router.get("/profiles", response_model=list[ProfileOut])
def list_profiles(
    current_user: User = Depends(deps.get_current_active_user),
    service: ProfileService = Depends(get_profile_service),
):
    """Список профилей пользователя."""

    return service.list_for_user(current_user.id)


@router.post("/profiles", response_model=ProfileOut, status_code=status.HTTP_201_CREATED)
def create_profile(
    payload: ProfileCreate,
    current_user: User = Depends(deps.get_current_active_user),
    service: ProfileService = Depends(get_profile_service),
):
    """Создать профиль."""

    return service.create(user_id=current_user.id, profile_in=payload)


@router.patch("/profiles/{profile_id}", response_model=ProfileOut)
def update_profile(
    profile_id: int,
    payload: ProfileUpdate,
    current_user: User = Depends(deps.get_current_active_user),
    service: ProfileService = Depends(get_profile_service),
):
    """Обновить профиль."""

    profile = service.get(profile_id, current_user.id)
    if not profile:
        raise HTTPException(status_code=404, detail="Профиль не найден")
    return service.update(profile, payload)


@router.delete("/profiles/{profile_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_profile(
    profile_id: int,
    current_user: User = Depends(deps.get_current_active_user),
    service: ProfileService = Depends(get_profile_service),
):
    """Удалить профиль."""

    profile = service.get(profile_id, current_user.id)
    if not profile:
        raise HTTPException(status_code=404, detail="Профиль не найден")
    service.delete(profile)
    return None
