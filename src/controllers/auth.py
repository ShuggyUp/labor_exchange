from fastapi import HTTPException, status
from schemas import LoginSchema, TokensOutSchema
from sqlalchemy.ext.asyncio import AsyncSession
from queries import user as user_queries
from core.security import (
    verify_password,
    create_token,
    decode_token,
)


def __create_tokens_with_out_schema(data: str) -> TokensOutSchema:
    access_token = create_token({"sub": data})
    refresh_token = create_token({"sub": data})

    return TokensOutSchema(
        message="Login successful",
        access_token=access_token,
        refresh_token=refresh_token,
        token_type="Bearer",
    )


async def login(login: LoginSchema, db: AsyncSession) -> TokensOutSchema:
    user = await user_queries.get_by_email(db=db, email=login.email)

    if user is None or not verify_password(login.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Некорректное имя пользователя или пароль",
        )

    return __create_tokens_with_out_schema(user.email)


async def get_new_tokens_by_refresh_token(refresh_token: str) -> TokensOutSchema:
    token = decode_token(refresh_token)
    return __create_tokens_with_out_schema(token.get("sub"))
