import pytest
from models import User
from queries import job as job_query
from fixtures.jobs import JobFactory
from schemas import JobInSchema


@pytest.mark.asyncio
async def test_get_all_available_jobs_for_company(
    sa_session, mock_own_company: User, mock_another_company: User
):
    own_company_job = JobFactory.build()
    own_company_job.user_id = mock_own_company.id
    sa_session.add(own_company_job)

    another_company_job = JobFactory.build()
    another_company_job.user_id = mock_another_company.id
    another_company_job.is_active = False
    sa_session.add(another_company_job)

    sa_session.flush()

    all_available_jobs = await job_query.get_all_available_jobs_for_company(
        db=sa_session, user_id=mock_own_company.id
    )
    assert all_available_jobs
    assert len(all_available_jobs) == 1
    assert all_available_jobs[0] == own_company_job


@pytest.mark.asyncio
async def test_get_null_list_jobs_for_company(sa_session, mock_own_company: User):
    null_list_jobs = await job_query.get_all_available_jobs_for_company(
        db=sa_session, user_id=mock_own_company.id
    )
    assert null_list_jobs == []


@pytest.mark.asyncio
async def test_get_all_available_jobs_for_user(sa_session, mock_own_company: User):
    active_job = JobFactory.build()
    active_job.user_id = mock_own_company.id
    active_job.is_active = True
    sa_session.add(active_job)

    inactive_job = JobFactory.build()
    inactive_job.user_id = mock_own_company.id
    inactive_job.is_active = False
    sa_session.add(inactive_job)

    sa_session.flush()

    all_available_jobs = await job_query.get_all_available_jobs_for_user(db=sa_session)
    assert all_available_jobs
    assert len(all_available_jobs) == 1
    assert all_available_jobs[0] == active_job


@pytest.mark.asyncio
async def test_get_null_list_jobs_for_user(sa_session):
    null_list_jobs = await job_query.get_all_available_jobs_for_user(db=sa_session)
    assert null_list_jobs == []


@pytest.mark.asyncio
async def test_get_available_job_by_id_for_user(sa_session, mock_own_company: User):
    available_job = JobFactory.build()
    available_job.user_id = mock_own_company.id
    available_job.is_active = True
    sa_session.add(available_job)
    sa_session.flush()

    current_job = await job_query.get_available_job_by_id_for_user(
        db=sa_session, job_id=available_job.id
    )
    assert current_job is not None
    assert current_job.id == available_job.id


@pytest.mark.asyncio
async def test_get_null_job_by_non_exist_id_for_user(sa_session):
    non_exist_id = 10
    non_exist_job = await job_query.get_available_job_by_id_for_user(
        db=sa_session, job_id=non_exist_id
    )
    assert non_exist_job is None


@pytest.mark.asyncio
async def test_get_unavailable_job_by_id_for_user(sa_session, mock_user: User):
    unavailable_job = JobFactory.build()
    unavailable_job.user_id = mock_user.id
    unavailable_job.is_active = False
    sa_session.add(unavailable_job)
    sa_session.flush()

    unavailable_job = await job_query.get_available_job_by_id_for_user(
        db=sa_session, job_id=unavailable_job.id
    )
    assert unavailable_job is None


@pytest.mark.asyncio
async def test_get_available_job_by_id_for_company(sa_session, mock_own_company: User):
    available_job = JobFactory.build()
    available_job.user_id = mock_own_company.id
    sa_session.add(available_job)
    sa_session.flush()

    current_job = await job_query.get_available_job_by_id_for_company(
        db=sa_session, job_id=available_job.id, user_id=available_job.user_id
    )
    assert current_job is not None
    assert current_job.id == available_job.id
    assert current_job.user_id == available_job.user_id


@pytest.mark.asyncio
async def test_get_null_job_by_non_exist_id_for_company(
    sa_session, mock_own_company: User
):
    non_exist_id = 10
    non_exist_job = await job_query.get_available_job_by_id_for_company(
        db=sa_session, job_id=non_exist_id, user_id=mock_own_company.id
    )
    assert non_exist_job is None


@pytest.mark.asyncio
async def test_get_unavailable_job_by_id_for_company(
    sa_session, mock_own_company: User, mock_another_company: User
):
    unavailable_job = JobFactory.build()
    unavailable_job.user_id = mock_another_company.id
    unavailable_job.is_active = False
    sa_session.add(unavailable_job)
    sa_session.flush()

    unavailable_job = await job_query.get_available_job_by_id_for_company(
        db=sa_session, job_id=unavailable_job.id, user_id=mock_own_company.id
    )
    assert unavailable_job is None


@pytest.mark.asyncio
async def test_get_available_job_by_id_for_own_company_job(
    sa_session, mock_own_company: User
):
    available_job = JobFactory.build()
    available_job.user_id = mock_own_company.id
    sa_session.add(available_job)
    sa_session.flush()

    current_job = (
        await job_query.get_available_job_by_id_for_company_to_delete_or_update(
            db=sa_session, job_id=available_job.id, user_id=available_job.user_id
        )
    )
    assert current_job is not None
    assert current_job.id == available_job.id
    assert current_job.user_id == available_job.user_id


@pytest.mark.asyncio
async def test_get_null_job_by_non_exist_id_for_own_company_job(
    sa_session, mock_own_company: User
):
    non_exist_id = 10
    non_exist_job = (
        await job_query.get_available_job_by_id_for_company_to_delete_or_update(
            db=sa_session, job_id=non_exist_id, user_id=mock_own_company.id
        )
    )
    assert non_exist_job is None


@pytest.mark.asyncio
async def test_get_unavailable_job_by_id_for_own_company_job(
    sa_session, mock_own_company: User, mock_another_company: User
):
    unavailable_job = JobFactory.build()
    unavailable_job.user_id = mock_another_company.id
    unavailable_job.is_active = False
    sa_session.add(unavailable_job)
    sa_session.flush()

    unavailable_job = (
        await job_query.get_available_job_by_id_for_company_to_delete_or_update(
            db=sa_session, job_id=unavailable_job.id, user_id=mock_own_company.id
        )
    )
    assert unavailable_job is None


@pytest.mark.asyncio
async def test_create_job(sa_session, mock_own_company: User):
    job = JobInSchema(
        title="Galera tech",
        description="точно не галера",
        salary_from=10000,
        salary_to=35000,
        is_active=True,
    )

    new_job = await job_query.create_job(
        sa_session, job_schema=job, user_id=mock_own_company.id
    )
    assert new_job is not None
    assert new_job.title == "Galera tech"
    assert new_job.user_id == mock_own_company.id


@pytest.mark.asyncio
async def test_update_job(sa_session, mock_own_company: User):
    job = JobFactory.build()
    job.user_id = mock_own_company.id
    sa_session.add(job)
    sa_session.flush()

    job.name = "Ne galera tech"
    updated_job = await job_query.update_job(sa_session, job=job)
    assert job.id == updated_job.id
    assert updated_job.name == job.name


@pytest.mark.asyncio
async def test_delete_job(sa_session, mock_own_company: User):
    job = JobFactory.build()
    job.user_id = mock_own_company.id
    sa_session.add(job)
    sa_session.flush()

    deleted_job = await job_query.delete_job(sa_session, job=job)
    assert job.id == deleted_job.id
