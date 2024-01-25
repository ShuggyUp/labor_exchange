from fastapi import Depends, HTTPException, status
from dependencies.user import get_current_user
from models import User


async def access_verification_for_company(
    current_user: User = Depends(get_current_user),
) -> None:
    if not current_user.is_company:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Нет доступа")


async def access_verification_for_user(
    current_user: User = Depends(get_current_user),
) -> None:
    if current_user.is_company:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Нет доступа")
