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


class UserUpdateSchema(BaseModel):
    name: Optional[str] = Field(default=None)
    email: Optional[EmailStr] = Field(default=None)
    is_company: Optional[bool] = Field(default=None)


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
