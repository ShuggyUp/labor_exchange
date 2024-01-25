from fastapi import HTTPException, status
from schemas import UserSchema, UserInSchema, UserUpdateSchema
from sqlalchemy.ext.asyncio import AsyncSession
from queries import user as user_queries
from models import User


async def create_user(user: UserInSchema, db: AsyncSession) -> UserSchema:
    user = await user_queries.create_user(db=db, user_schema=user)
    return UserSchema.from_orm(user)


async def update_user(
    user_id: int, user: UserUpdateSchema, db: AsyncSession, current_user: User
) -> UserSchema:
    old_user = await user_queries.get_by_id(db=db, user_id=user_id)
    same_email_in_db = await user_queries.get_by_email(db=db, email=user.email)

    if same_email_in_db:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="Такой email уже существует"
        )

    if not old_user or old_user.email != current_user.email:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Пользователь не найден"
        )

    old_user.name = user.name if user.name is not None else old_user.name
    old_user.email = user.email if user.email is not None else old_user.email
    old_user.is_company = (
        user.is_company if user.is_company is not None else old_user.is_company
    )

    new_user = await user_queries.update_user(db=db, user=old_user)
    return UserSchema.from_orm(new_user)
