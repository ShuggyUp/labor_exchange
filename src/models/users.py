import datetime

from sqlalchemy.orm import relationship

from db_connection import Base
from sqlalchemy import Column, Integer, String, Boolean, DateTime


class User(Base):
    __tablename__ = "users"

    id = Column(
        Integer,
        primary_key=True,
        autoincrement=True,
        comment="Идентификатор задачи",
        unique=True,
    )
    email = Column(String, comment="Email адрес", unique=True)
    name = Column(String, comment="Имя пользователя")
    hashed_password = Column(String, comment="Зашифрованный пароль")
    is_company = Column(Boolean, comment="Флаг компании")
    created_at = Column(
        DateTime, comment="Время создания записи", default=datetime.datetime.utcnow
    )

    jobs = relationship("Job", back_populates="user")
    responses = relationship("Response", back_populates="user")
