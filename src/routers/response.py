from typing import List
from fastapi import APIRouter, Depends, Query, Body
from schemas import ResponseSchema, ResponseInSchema
from dependencies import (
    get_db,
    get_current_user,
    access_verification_for_company,
    access_verification_for_user,
)
from sqlalchemy.ext.asyncio import AsyncSession
from models import User
from controllers import response as response_controller

router = APIRouter(prefix="/responses", tags=["responses"])


@router.get(
    "",
    response_model=List[ResponseSchema],
    dependencies=[Depends(access_verification_for_company)],
)
async def get_responses_by_job_id(
    job_id: int = Query(...),
    limit: int = Query(default=100),
    skip: int = Query(default=0),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Получает все отклики на вакансию по ее идентификатору
    """
    return await response_controller.get_responses_by_job_id(
        job_id=job_id, limit=limit, skip=skip, db=db, current_user=current_user
    )


@router.post(
    "",
    response_model=ResponseSchema,
    dependencies=[Depends(access_verification_for_user)],
)
async def create_response(
    job: ResponseInSchema = Body(...),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Создает отклик на вакансию
    """
    return await response_controller.create_response(
        job=job, db=db, current_user=current_user
    )
