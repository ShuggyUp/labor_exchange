from models import Job
from schemas import JobInSchema
from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, or_
from sqlalchemy.orm.query import Query


async def __save_instance_db(db: AsyncSession, job: Job) -> Job:
    db.add(job)
    await db.commit()
    await db.refresh(job)
    return job


async def __execute_sql_with_many_results(db: AsyncSession, query: Query) -> List[Job]:
    res = await db.execute(query)
    return res.scalars().all()


async def __execute_sql_with_one_result(db: AsyncSession, query: Query) -> Job:
    res = await db.execute(query)
    return res.scalars().first()


async def create_job(db: AsyncSession, job_schema: JobInSchema, user_id: int) -> Job:
    job = Job(
        user_id=user_id,
        title=job_schema.title,
        description=job_schema.description,
        salary_from=job_schema.salary_from,
        salary_to=job_schema.salary_to,
        is_active=job_schema.is_active,
    )
    return await __save_instance_db(db, job)


async def update_job(db: AsyncSession, job: Job) -> Job:
    return await __save_instance_db(db, job)


async def delete_job(db: AsyncSession, job: Job) -> Job:
    await db.delete(job)
    await db.commit()
    return job


async def get_all_available_jobs_for_user(
    db: AsyncSession, limit: int = 100, skip: int = 0
) -> List[Job]:
    query = select(Job).where(Job.is_active.is_(True)).limit(limit).offset(skip)
    return await __execute_sql_with_many_results(db, query)


async def get_all_available_jobs_for_company(
    db: AsyncSession, user_id: int, limit: int = 100, skip: int = 0
) -> List[Job]:
    query = (
        select(Job)
        .where(or_(Job.is_active.is_(True), Job.user_id == user_id))
        .limit(limit)
        .offset(skip)
    )
    return await __execute_sql_with_many_results(db, query)


async def get_available_job_by_id_for_user(
    db: AsyncSession, job_id: int
) -> Optional[Job]:
    query = select(Job).where(Job.id == job_id, Job.is_active.is_(True))
    return await __execute_sql_with_one_result(db, query)


async def get_available_job_by_id_for_company(
    db: AsyncSession, job_id: int, user_id: int
) -> Optional[Job]:
    query = select(Job).where(
        Job.id == job_id, or_(Job.is_active.is_(True), Job.user_id == user_id)
    )
    return await __execute_sql_with_one_result(db, query)


async def get_available_job_by_id_for_company_to_delete_or_update(
    db: AsyncSession, job_id: int, user_id: int
) -> Optional[Job]:
    query = select(Job).where(Job.id == job_id, Job.user_id == user_id)
    return await __execute_sql_with_one_result(db, query)
