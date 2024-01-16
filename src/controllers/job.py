from typing import List
from fastapi import HTTPException, status
from schemas import JobSchema, JobInSchema, JobUpdateSchema
from sqlalchemy.ext.asyncio import AsyncSession
from queries import job as job_queries
from models import User


async def get_jobs_for_user_or_company(
    limit: int, skip: int, db: AsyncSession, current_user: User
) -> List[JobSchema]:
    if current_user.is_company:
        jobs = await job_queries.get_all_available_jobs_for_company(
            db=db, limit=limit, skip=skip, user_id=current_user.id
        )
    else:
        jobs = await job_queries.get_all_available_jobs_for_user(
            db=db, limit=limit, skip=skip
        )
    return jobs


async def get_job_by_id_for_user_or_company(
    job_id: int, db: AsyncSession, current_user: User
) -> JobSchema:
    if current_user.is_company:
        job = await job_queries.get_available_job_by_id_for_company(
            db=db, job_id=job_id, user_id=current_user.id
        )
    else:
        job = await job_queries.get_available_job_by_id_for_user(db=db, job_id=job_id)

    if job is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Запись не найдена"
        )
    return job


async def create_job(
    job: JobInSchema, db: AsyncSession, current_user: User
) -> JobSchema:
    if not current_user.is_company:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Нет доступа")

    job = await job_queries.create_job(db=db, job_schema=job, user_id=current_user.id)
    return JobSchema.from_orm(job)


async def update_available_job(
    job_id: int, job: JobUpdateSchema, db: AsyncSession, current_user: User
) -> JobSchema:
    if not current_user.is_company:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Нет доступа")

    old_job = await job_queries.get_available_job_by_id_for_company_to_delete_or_update(
        db=db, job_id=job_id, user_id=current_user.id
    )

    if old_job is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Запись не найдена"
        )

    old_job.title = job.title if job.title is not None else old_job.title
    old_job.description = (
        job.description if job.description is not None else old_job.description
    )
    old_job.salary_from = job.salary_from
    old_job.salary_to = job.salary_to

    new_job = await job_queries.update_job(db=db, job=old_job)

    return JobSchema.from_orm(new_job)


async def delete_available_job(
    job_id: int, db: AsyncSession, current_user: User
) -> JobSchema:
    if not current_user.is_company:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Нет доступа")

    job = await job_queries.get_available_job_by_id_for_company_to_delete_or_update(
        db=db, job_id=job_id, user_id=current_user.id
    )
    if job is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Запись не найдена"
        )

    deleted_job = await job_queries.delete_job(db=db, job=job)
    return JobSchema.from_orm(deleted_job)
