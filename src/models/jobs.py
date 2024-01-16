import datetime

from db_settings import Base
from sqlalchemy import Column, Integer, String, DECIMAL, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship


class Job(Base):
    __tablename__ = "jobs"

    id = Column(
        Integer, primary_key=True, autoincrement=True, comment="Идентификатор вакансии"
    )
    user_id = Column(
        Integer, ForeignKey("users.id"), comment="Идентификатор пользователя"
    )

    title = Column(String, nullable=False, comment="Название вакансии")
    description = Column(String, nullable=False, comment="Описание вакансии")
    salary_from = Column(DECIMAL, comment="Зарплата от")
    salary_to = Column(DECIMAL, comment="Зарплата до")
    is_active = Column(Boolean, default=True, comment="Активна ли вакансия")
    created_at = Column(
        DateTime, default=datetime.datetime.utcnow, comment="Дата создания записи"
    )

    user = relationship("User", back_populates="jobs")
    responses = relationship("Response", back_populates="job")
