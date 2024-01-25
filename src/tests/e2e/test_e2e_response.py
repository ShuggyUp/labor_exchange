import pytest
from fastapi import status
from fixtures.responses import ResponseFactory
from fixtures.jobs import JobFactory
from models import User
from schemas import ResponseInSchema


@pytest.mark.asyncio
async def test_get_responses_by_job_id_for_company(
    sa_session, mock_app_company, mock_user: User, mock_own_company: User
):
    job = JobFactory.build()
    job.user_id = mock_own_company.id
    sa_session.add(job)

    job_response = ResponseFactory.build()
    job_response.job_id = job.id
    job_response.user_id = mock_user.id
    sa_session.add(job_response)

    sa_session.flush()

    responses = await mock_app_company.get(url=f"/responses?job_id={job.id}")

    assert responses.status_code == status.HTTP_200_OK
    assert len(responses.json()) == 1


@pytest.mark.asyncio
async def test_get_responses_by_job_id_for_user(
    sa_session, mock_app_user, mock_own_company: User
):
    job = JobFactory.build()
    job.user_id = mock_own_company.id
    sa_session.add(job)
    sa_session.flush()

    responses = await mock_app_user.get(url=f"/responses?job_id={job.id}")

    assert responses.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.asyncio
async def test_post_response_by_user(sa_session, mock_app_user, mock_own_company: User):
    job = JobFactory.build()
    job.user_id = mock_own_company.id
    job.is_active = True
    sa_session.add(job)
    sa_session.flush()

    job_response = ResponseInSchema(job_id=job.id, message="Тестовое сообщение")

    response = await mock_app_user.post(url="/responses", json=job_response.dict())

    assert response.status_code == status.HTTP_200_OK
    assert response.json()["job_id"] == job.id


@pytest.mark.asyncio
async def test_post_response_by_company(
    sa_session, mock_app_company, mock_own_company: User
):
    job = JobFactory.build()
    job.user_id = mock_own_company.id
    job.is_active = True
    sa_session.add(job)
    sa_session.flush()

    job_response = ResponseInSchema(job_id=job.id, message="Тестовое сообщение")

    response = await mock_app_company.post(url="/responses", json=job_response.dict())

    assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.asyncio
async def test_post_response_by_not_existing_job(mock_app_user):
    job_response = ResponseInSchema(job_id=100, message="Тестовое сообщение")

    response = await mock_app_user.post(url="/responses", json=job_response.dict())

    assert response.status_code == status.HTTP_404_NOT_FOUND
