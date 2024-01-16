from typing import List
from fastapi import APIRouter, Depends, Query, Body
from schemas import JobSchema, JobInSchema, JobUpdateSchema
from dependencies import get_db, get_current_user
from sqlalchemy.ext.asyncio import AsyncSession
from models import User
from controllers import job as job_controller

router = APIRouter(prefix="/jobs", tags=["jobs"])


@router.get("", response_model=List[JobSchema])
async def get_jobs(
    limit: int = Query(default=100),
    skip: int = Query(default=0),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Получает вакансии по заданным лимитам
    """
    return await job_controller.get_jobs_for_user_or_company(
        limit=limit, skip=skip, db=db, current_user=current_user
    )


@router.get("/by_id", response_model=JobSchema)
async def get_job_by_id(
    job_id: int = Query(...),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Получает вакансию по ее идентификатору
    """
    return await job_controller.get_job_by_id_for_user_or_company(
        job_id=job_id, db=db, current_user=current_user
    )


@router.post("", response_model=JobSchema)
async def create_job(
    job: JobInSchema = Body(...),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Создает вакансию
    """
    return await job_controller.create_job(job=job, db=db, current_user=current_user)


@router.put("", response_model=JobSchema)
async def update_job(
    job_id: int = Query(...),
    job: JobUpdateSchema = Body(...),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Обновляет данные о вакансии
    """
    return await job_controller.update_available_job(
        job_id=job_id, job=job, db=db, current_user=current_user
    )


@router.delete("", response_model=JobSchema)
async def delete_job(
    job_id: int = Query(...),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Удаляет вакансию
    """
    return await job_controller.delete_available_job(
        job_id=job_id, db=db, current_user=current_user
    )
