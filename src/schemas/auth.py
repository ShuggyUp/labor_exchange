from pydantic import BaseModel, EmailStr, Field


class AccessTokenSchema(BaseModel):
    """
    Класс схемы access токена
    """

    access_token: str = Field(...)
    token_type: str = Field(...)


class LoginSchema(BaseModel):
    """
    Класс схемы для входа в систему
    """

    email: EmailStr = Field(...)
    password: str = Field(...)

    class Config:
        schema_extra = {
            "example": {
                "email": "ivanov@mail.ru",
                "password": "veryhardpassword",
            }
        }


class TokensOutSchema(AccessTokenSchema):
    """
    Класс схемы для вывода токенов
    """

    message: str = Field(...)
    refresh_token: str = Field(...)

    class Config:
        schema_extra = {
            "example": {
                "message": "Successful",
                "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6Ikp",
                "refresh_token": "JzdWIsInRpbOiIyMDI0LTA4IDA4OjQ5",
                "token_type": "bearer",
            }
        }
