from models import Response, Job
from schemas import ResponseInSchema
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select


async def create_response(
    db: AsyncSession, response_schema: ResponseInSchema, user_id: int
) -> Response:
    response = Response(
        user_id=user_id, job_id=response_schema.job_id, message=response_schema.message
    )
    db.add(response)
    await db.commit()
    await db.refresh(response)
    return response


async def get_responses_by_job_id(
    db: AsyncSession, job_id: int, user_id: int, limit: int = 100, skip: int = 0
) -> List[Response]:
    query = (
        select(Response)
        .where(
            Response.job_id == job_id,
            Response.job_id.in_(select(Job.id).where(Job.user_id == user_id)),
        )
        .limit(limit)
        .offset(skip)
    )
    res = await db.execute(query)
    return res.scalars().all()
