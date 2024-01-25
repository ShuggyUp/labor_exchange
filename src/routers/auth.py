from fastapi import APIRouter, Depends, Body, Query
from sqlalchemy.ext.asyncio import AsyncSession
from schemas import LoginSchema, TokensOutSchema
from dependencies import get_db
from controllers import auth as auth_controller


router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("", response_model=TokensOutSchema)
async def login(login: LoginSchema = Body(...), db: AsyncSession = Depends(get_db)):
    """
    Входит в систему по введенным данным
    """
    return await auth_controller.login(login=login, db=db)


@router.post("/refresh_token", response_model=TokensOutSchema)
async def get_new_tokens(refresh_token: str = Query(...)):
    """
    Генерирует новую пару access и refresh токенов
    """
    return await auth_controller.get_new_tokens_by_refresh_token(
        refresh_token=refresh_token
    )
