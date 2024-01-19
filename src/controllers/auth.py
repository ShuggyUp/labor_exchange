from datetime import datetime
from fastapi import HTTPException, status
from schemas import LoginSchema, TokensOutSchema
from sqlalchemy.ext.asyncio import AsyncSession
from queries import user as user_queries
from core.security import (
    verify_password,
    create_access_token,
    create_refresh_token,
    decode_token,
)


async def login(login: LoginSchema, db: AsyncSession) -> TokensOutSchema:
    user = await user_queries.get_by_email(db=db, email=login.email)

    if user is None or not verify_password(login.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Некорректное имя пользователя или пароль",
        )

    access_token = create_access_token({"sub": user.email})
    refresh_token = create_refresh_token({"sub": user.email})

    return TokensOutSchema(
        message="Login successful",
        access_token=access_token,
        refresh_token=refresh_token,
        token_type="Bearer",
    )


async def get_new_tokens_by_refresh_token(refresh_token: str) -> TokensOutSchema:
    cred_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED, detail="Credentials are not valid"
    )

    token = decode_token(refresh_token)
    exp_token_time = datetime.strptime(token.get("time"), "%Y-%m-%d %H:%M:%S.%f")
    if exp_token_time > datetime.utcnow():
        access_token = create_access_token({"sub": token.get("sub")})
        refresh_token = create_refresh_token({"sub": token.get("sub")})
    else:
        raise cred_exception

    return TokensOutSchema(
        message="Creating tokens successful",
        access_token=access_token,
        refresh_token=refresh_token,
        token_type="Bearer",
    )
