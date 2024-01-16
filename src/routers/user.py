from typing import List
from fastapi import APIRouter, Depends, Query, Body
from schemas import UserSchema, UserInSchema, UserUpdateSchema
from dependencies import get_db, get_current_user
from sqlalchemy.ext.asyncio import AsyncSession
from queries import user as user_queries
from models import User
from controllers import user as user_controller

router = APIRouter(prefix="/users", tags=["users"])


@router.get("", response_model=List[UserSchema])
async def get_users(
    limit: int = Query(default=100),
    skip: int = Query(default=0),
    db: AsyncSession = Depends(get_db),
):
    """
    Получает всех пользователей
    """
    return await user_queries.get_all(db=db, limit=limit, skip=skip)


@router.post("", response_model=UserSchema)
async def create_user(
    user: UserInSchema = Body(...), db: AsyncSession = Depends(get_db)
):
    """
    Создает пользователя
    """
    return await user_controller.create_user(user=user, db=db)


@router.put("", response_model=UserSchema)
async def update_user(
    user_id: int = Query(...),
    user: UserUpdateSchema = Body(...),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Обновляет пользователя
    """
    return await user_controller.update_user(
        user_id=user_id, user=user, db=db, current_user=current_user
    )
