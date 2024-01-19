import datetime
from fastapi import Request, HTTPException, status
from fastapi.security import HTTPBearer
from passlib.context import CryptContext
from jose import jwt
from config import token_settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(password: str, hash: str) -> bool:
    return pwd_context.verify(password, hash)


def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    to_encode.update(
        {
            "time": str(
                datetime.datetime.utcnow()
                + datetime.timedelta(minutes=token_settings.access_token_expire_minutes)
            )
        }
    )
    return jwt.encode(
        to_encode, token_settings.secret_key, algorithm=token_settings.algorithm
    )


def create_refresh_token(data: dict) -> str:
    to_encode = data.copy()
    to_encode.update(
        {
            "time": str(
                datetime.datetime.utcnow()
                + datetime.timedelta(
                    minutes=token_settings.refresh_token_expire_minutes
                )
            )
        }
    )
    return jwt.encode(
        to_encode, token_settings.secret_key, algorithm=token_settings.algorithm
    )


def decode_token(token: str):
    try:
        encoded_jwt = jwt.decode(
            token, token_settings.secret_key, algorithms=[token_settings.algorithm]
        )
    except jwt.JWSError:
        return None
    return encoded_jwt


class JWTBearer(HTTPBearer):
    def __init__(self, auto_error: bool = True):
        super(JWTBearer, self).__init__(auto_error=auto_error)

    async def __call__(self, request: Request):
        credentials = await super(JWTBearer, self).__call__(request)
        exp = HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Invalid auth token"
        )
        if credentials:
            token = decode_token(credentials.credentials)
            if token is None:
                raise exp
            return credentials.credentials
        else:
            raise exp
