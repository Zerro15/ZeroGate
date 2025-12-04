"""Роуты для пользователей."""
from fastapi import APIRouter, Depends

from backend.app.api import deps
from backend.app.models.user import User
from backend.app.schemas.user import UserOut

router = APIRouter()


@router.get("/users/me", response_model=UserOut)
def read_users_me(current_user: User = Depends(deps.get_current_active_user)):
    """Возвращает текущего активного пользователя."""

    return current_user
