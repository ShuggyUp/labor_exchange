import datetime
from typing import Optional
from pydantic import BaseModel, validator, Field


class JobSchema(BaseModel):
    """
    Класс схемы на вывод job
    """

    id: int = Field(...)
    user_id: int = Field(...)
    title: str = Field(...)
    description: str = Field(...)
    salary_from: Optional[float] = Field(default=None)
    salary_to: Optional[float] = Field(default=None)
    is_active: bool = Field(...)
    created_at: datetime.datetime = Field(...)

    class Config:
        orm_mode = True


class JobUpdateSchema(BaseModel):
    """
    Класс схемы на обновление job
    """

    title: Optional[str] = Field(default=None)
    description: Optional[str] = Field(default=None)
    salary_from: Optional[float] = Field(default=None, ge=0)
    salary_to: Optional[float] = Field(default=None, ge=0)
    is_active: Optional[bool] = Field(default=None)

    @validator("salary_to")
    def salary_comparison(cls, v, values, **kwargs):
        if values["salary_from"] > v:
            raise ValueError("salary_from, должна быть меньше salary_to!")
        return v


class JobInSchema(BaseModel):
    """
    Класс схемы на прием данных для создания job
    """

    title: str = Field(...)
    description: str = Field(...)
    salary_from: Optional[float] = Field(default=None, ge=0)
    salary_to: Optional[float] = Field(default=None, ge=0)
    is_active: Optional[bool] = Field(default=None)

    @validator("salary_to")
    def salary_comparison(cls, v, values, **kwargs):
        if values["salary_from"] > v:
            raise ValueError("salary_from, должна быть меньше salary_to!")
        return v
