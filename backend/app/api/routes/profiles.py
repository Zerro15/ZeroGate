"""Connection profile endpoints."""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_session
from app.models.profile import Profile
from app.schemas.profile import ProfileCreate, ProfileRead, ProfileUpdate
from app.services.deps import get_current_user
from app.services.auth import require_active_user

router = APIRouter(prefix="/profiles", tags=["profiles"])


@router.get("/", response_model=list[ProfileRead])
async def list_profiles(
    session: AsyncSession = Depends(get_session), current_user=Depends(get_current_user)
):
    await require_active_user(current_user)
    result = await session.execute(select(Profile).where(Profile.user_id == current_user.id))
    return result.scalars().all()


@router.post("/", response_model=ProfileRead, status_code=status.HTTP_201_CREATED)
async def create_profile(
    payload: ProfileCreate,
    session: AsyncSession = Depends(get_session),
    current_user=Depends(get_current_user),
):
    await require_active_user(current_user)
    if payload.user_id != current_user.id and not current_user.is_admin:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Cannot assign to other user")
    profile = Profile(
        name=payload.name,
        server=payload.server,
        port=payload.port,
        protocol=payload.protocol,
        encryption=payload.encryption,
        is_active=payload.is_active,
        user_id=payload.user_id,
    )
    session.add(profile)
    await session.commit()
    await session.refresh(profile)
    return profile


@router.patch("/{profile_id}", response_model=ProfileRead)
async def update_profile(
    profile_id: int,
    payload: ProfileUpdate,
    session: AsyncSession = Depends(get_session),
    current_user=Depends(get_current_user),
):
    await require_active_user(current_user)
    profile = await session.get(Profile, profile_id)
    if not profile or profile.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Profile not found")
    for field, value in payload.dict(exclude_unset=True).items():
        setattr(profile, field, value)
    await session.commit()
    await session.refresh(profile)
    return profile


@router.delete("/{profile_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_profile(
    profile_id: int,
    session: AsyncSession = Depends(get_session),
    current_user=Depends(get_current_user),
):
    await require_active_user(current_user)
    profile = await session.get(Profile, profile_id)
    if not profile or profile.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Profile not found")
    await session.delete(profile)
    await session.commit()
    return None
