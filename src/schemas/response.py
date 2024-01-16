from typing import Optional
from pydantic import BaseModel, Field


class ResponseSchema(BaseModel):
    """
    Класс схемы на вывод данных job
    """

    id: int = Field(...)
    user_id: int = Field(...)
    job_id: int = Field(...)
    message: Optional[str] = Field(defaut=None)

    class Config:
        orm_mode = True


class ResponseInSchema(BaseModel):
    """
    Класс схемы на прием данных для создания job
    """

    job_id: int = Field(...)
    message: Optional[str] = Field(defaut=None)
