import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr, validator, constr, Field


class UserSchema(BaseModel):
    id: int = Field(...)
    name: str = Field(...)
    email: EmailStr = Field(...)
    is_company: bool = Field(...)
    created_at: datetime.datetime = Field(...)

    class Config:
        orm_mode = True

        schema_extra = {
            "example": {
                "id": 18,
                "name": "Иван Иванович Петров",
                "email": "petrov@mail.ru",
                "is_company": False,
                "created_at": "2024-01-17T17:26:15.814Z",
            }
        }


class UserUpdateSchema(BaseModel):
    name: Optional[str] = Field(default=None)
    email: Optional[EmailStr] = Field(default=None)
    is_company: Optional[bool] = Field(default=None)

    class Config:
        schema_extra = {
            "example": {
                "name": "Иван Иванович Иванов",
                "email": "ivanov@mail.ru",
                "is_company": False,
            }
        }


class UserInSchema(BaseModel):
    name: str = Field(...)
    email: EmailStr = Field(...)
    password: constr(min_length=8) = Field(...)
    password2: str = Field(...)
    is_company: bool = Field(default=False)

    @validator("password2")
    def password_match(cls, v, values, **kwargs):
        if "password" in values and v != values["password"]:
            raise ValueError("Пароли не совпадают")
        return v

    class Config:
        schema_extra = {
            "example": {
                "name": "Иван Иванович Иванов",
                "email": "ivanov@mail.ru",
                "password": "veryhardpassword",
                "password2": "veryhardpassword",
                "is_company": False,
            }
        }
