import pytest
from fastapi import status
from pydantic import ValidationError
from fixtures.jobs import JobFactory
from schemas import JobInSchema, JobUpdateSchema
from models import User


@pytest.mark.asyncio
async def test_get_available_jobs_for_company(
    sa_session, mock_app_company, mock_own_company: User
):
    available_job = JobFactory.build()
    available_job.user_id = mock_own_company.id
    sa_session.add(available_job)
    sa_session.flush()

    responses = await mock_app_company.get(url=f"/jobs")

    assert responses.status_code == status.HTTP_200_OK
    assert len(responses.json()) == 1


@pytest.mark.asyncio
async def test_get_null_list_jobs_for_company(mock_app_company):
    responses = await mock_app_company.get(url=f"/jobs")

    assert responses.status_code == status.HTTP_200_OK
    assert len(responses.json()) == 0


@pytest.mark.asyncio
async def test_get_available_jobs_for_user(
    sa_session, mock_app_user, mock_own_company: User
):
    active_job = JobFactory.build()
    active_job.user_id = mock_own_company.id
    active_job.is_active = True
    sa_session.add(active_job)

    inactive_job = JobFactory.build()
    inactive_job.user_id = mock_own_company.id
    inactive_job.is_active = False
    sa_session.add(inactive_job)

    sa_session.flush()

    responses = await mock_app_user.get(url=f"/jobs")

    assert responses.status_code == status.HTTP_200_OK
    assert len(responses.json()) == 1


@pytest.mark.asyncio
async def test_get_null_list_jobs_for_user(mock_app_user):
    responses = await mock_app_user.get(url=f"/jobs")

    assert responses.status_code == status.HTTP_200_OK
    assert len(responses.json()) == 0


@pytest.mark.asyncio
async def test_get_available_job_by_id_for_company(
    sa_session, mock_app_company, mock_own_company: User
):
    available_job = JobFactory.build()
    available_job.user_id = mock_own_company.id
    sa_session.add(available_job)
    sa_session.flush()

    response = await mock_app_company.get(url=f"/jobs/by_id?job_id={available_job.id}")

    assert response.status_code == status.HTTP_200_OK
    assert response.json()["id"] == available_job.id


@pytest.mark.asyncio
async def test_get_available_job_by_id_for_user(
    sa_session, mock_app_user, mock_own_company: User
):
    available_job = JobFactory.build()
    available_job.user_id = mock_own_company.id
    available_job.is_active = True
    sa_session.add(available_job)
    sa_session.flush()

    response = await mock_app_user.get(url=f"/jobs/by_id?job_id={available_job.id}")

    assert response.status_code == status.HTTP_200_OK
    assert response.json()["id"] == available_job.id


@pytest.mark.asyncio
async def test_get_non_exist_job_by_id(mock_app_user):
    response = await mock_app_user.get(url="/jobs/by_id?job_id=10")

    assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.asyncio
async def test_create_job_by_company(mock_app_company):
    job = JobInSchema(
        title="Galera tech",
        description="точно не галера",
        salary_from=10000,
        salary_to=35000,
        is_active=True,
    )

    response = await mock_app_company.post(url="/jobs", json=job.dict())

    assert response.status_code == status.HTTP_200_OK
    assert response.json()["title"] == "Galera tech"


@pytest.mark.asyncio
async def test_create_job_by_company_with_wrong_salary_param(mock_app_company):
    with pytest.raises(ValidationError):
        job_with_wrong_salary_param = JobInSchema(
            title="Galera tech",
            description="точно не галера",
            salary_from=10000,
            salary_to=5000,
            is_active=True,
        )

        await mock_app_company.post(
            url="/jobs", json=job_with_wrong_salary_param.dict()
        )


@pytest.mark.asyncio
async def test_create_job_by_user(mock_app_user):
    job = JobInSchema(
        title="Galera tech",
        description="точно не галера",
        salary_from=10000,
        salary_to=35000,
        is_active=True,
    )

    response = await mock_app_user.post(url="/jobs", json=job.dict())

    assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.asyncio
async def test_update_job_by_company(
    sa_session, mock_app_company, mock_own_company: User
):
    job = JobFactory.build()
    job.user_id = mock_own_company.id
    sa_session.add(job)
    sa_session.flush()

    update_job = JobUpdateSchema(
        title="Galera tech",
        description="точно не галера",
        salary_from=10000,
        salary_to=35000,
        is_active=True,
    )

    response = await mock_app_company.put(
        url=f"/jobs?job_id={job.id}", json=update_job.dict()
    )

    assert response.status_code == status.HTTP_200_OK
    assert response.json()["title"] == "Galera tech"
    assert response.json()["id"] == job.id


@pytest.mark.asyncio
async def test_update_job_by_company_with_wrong_salary_param(
    sa_session, mock_app_company, mock_own_company: User
):
    with pytest.raises(ValidationError):
        job = JobFactory.build()
        job.user_id = mock_own_company.id
        sa_session.add(job)
        sa_session.flush()

        job_with_wrong_salary_param = JobUpdateSchema(
            title="Galera tech",
            description="точно не галера",
            salary_from=10000,
            salary_to=5000,
            is_active=True,
        )

        await mock_app_company.put(
            url=f"/jobs?job_id={job.id}", json=job_with_wrong_salary_param.dict()
        )


@pytest.mark.asyncio
async def test_update_job_by_user(mock_app_user):
    update_job = JobUpdateSchema(
        title="Galera tech",
        description="точно не галера",
        salary_from=10000,
        salary_to=35000,
        is_active=True,
    )

    response = await mock_app_user.put(url="/jobs?job_id=1", json=update_job.dict())

    assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.asyncio
async def test_update_job_by_company_with_wring_job_id(mock_app_company):
    update_job = JobUpdateSchema(
        title="Galera tech",
        description="точно не галера",
        salary_from=10000,
        salary_to=35000,
        is_active=True,
    )

    response = await mock_app_company.put(url="/jobs?job_id=10", json=update_job.dict())

    assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.asyncio
async def test_delete_job_by_company(
    sa_session, mock_app_company, mock_own_company: User
):
    job = JobFactory.build()
    job.user_id = mock_own_company.id
    sa_session.add(job)
    sa_session.flush()

    response = await mock_app_company.delete(url=f"/jobs?job_id={job.id}")

    assert response.status_code == status.HTTP_200_OK
    assert response.json()["id"] == job.id


@pytest.mark.asyncio
async def test_delete_job_by_company_with_non_exist_key(mock_app_company):
    response = await mock_app_company.delete(url="/jobs?job_id=10")

    assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.asyncio
async def test_delete_job_by_user(mock_app_user):
    response = await mock_app_user.delete(url="/jobs?job_id=1")

    assert response.status_code == status.HTTP_403_FORBIDDEN
