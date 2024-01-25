from db_connection import Base
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship


class Response(Base):
    __tablename__ = "responses"

    id = Column(
        Integer, primary_key=True, autoincrement=True, comment="Идентификатор отклика"
    )
    user_id = Column(
        Integer, ForeignKey("users.id"), comment="Идентификатор пользователя"
    )
    job_id = Column(Integer, ForeignKey("jobs.id"), comment="Идентификатор вакансии")

    message = Column(String, comment="Сопроводительное письмо")

    user = relationship("User", back_populates="responses")
    job = relationship("Job", back_populates="responses")
