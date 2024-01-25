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

        schema_extra = {
            "example": {
                "id": 7,
                "user_id": 15,
                "title": "Python Developer",
                "description": "Разработка на Python сервисной части продукта.",
                "salary_from": 75000,
                "salary_to": 100000,
                "is_active": True,
                "created_at": "2024-01-17T16:43:25.814Z",
            }
        }


class SalaryValidator(BaseModel):
    """
    Класс для валидации диапазона зарплаты
    """

    salary_from: Optional[float] = Field(default=None, ge=0)
    salary_to: Optional[float] = Field(default=None, ge=0)

    @validator("salary_to")
    def salary_comparison(cls, v, values, **kwargs):
        if values["salary_from"] > v:
            raise ValueError("salary_from, должна быть меньше salary_to!")
        return v


class InSchemaExampleConfig(BaseModel):
    """
    Класс для имплементации показательной схемы
    """

    class Config:
        schema_extra = {
            "example": {
                "title": "Backend Developer",
                "description": "Разработка Backend части приложений, сайтов и внутренних сервисов.",
                "salary_from": 100000,
                "salary_to": 220000,
                "is_active": True,
                "created_at": "2024-01-17T17:28:15.814Z",
            }
        }


class JobUpdateSchema(SalaryValidator, InSchemaExampleConfig):
    """
    Класс схемы на обновление job
    """

    title: Optional[str] = Field(default=None)
    description: Optional[str] = Field(default=None)
    is_active: Optional[bool] = Field(default=None)


class JobInSchema(SalaryValidator, InSchemaExampleConfig):
    """
    Класс схемы на прием данных для создания job
    """

    title: str = Field(...)
    description: str = Field(...)
    is_active: Optional[bool] = Field(default=None)
