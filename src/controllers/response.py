from typing import List
from fastapi import HTTPException, status
from schemas import ResponseSchema, ResponseInSchema
from sqlalchemy.ext.asyncio import AsyncSession
from queries import response as response_queries
from queries import job as job_queries
from models import User


async def get_responses_by_job_id(
    job_id: int, limit: int, skip: int, db: AsyncSession, current_user: User
) -> List[ResponseSchema]:
    if not current_user.is_company:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Нет доступа")

    jobs = await response_queries.get_responses_by_job_id(
        db=db, job_id=job_id, user_id=current_user.id, limit=limit, skip=skip
    )
    return jobs


async def create_response(
    job: ResponseInSchema, db: AsyncSession, current_user: User
) -> ResponseSchema:
    if current_user.is_company:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Нет доступа")

    job_from_db = await job_queries.get_available_job_by_id_for_user(
        db=db, job_id=job.job_id
    )
    if job_from_db is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Запись работы не найдена"
        )

    user_response = await response_queries.get_responses_by_job_id(
        db=db, job_id=job.job_id, user_id=current_user.id
    )

    if user_response:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Вы уже откликнулись на эту вакансию",
        )

    job = await response_queries.create_response(
        db=db, response_schema=job, user_id=current_user.id
    )
    return ResponseSchema.from_orm(job)
