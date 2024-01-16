import pytest
from models import User
from queries import response as response_query
from fixtures.responses import ResponseFactory
from fixtures.jobs import JobFactory
from schemas import ResponseInSchema


@pytest.mark.asyncio
async def test_create_response_by_user(
    sa_session, mock_user: User, mock_own_company: User
):
    job = JobFactory.build()
    job.user_id = mock_own_company.id
    sa_session.add(job)
    sa_session.flush()

    response = ResponseInSchema(
        job_id=job.id,
        message="Пожожда, возьмите",
    )

    new_response = await response_query.create_response(
        sa_session, response_schema=response, user_id=mock_user.id
    )
    assert new_response is not None
    assert new_response.job_id == job.id
    assert new_response.user_id == mock_user.id


@pytest.mark.asyncio
async def test_get_all_available_responses_by_job_id_for_company(
    sa_session, mock_user: User, mock_own_company: User
):
    job = JobFactory.build()
    job.user_id = mock_own_company.id
    sa_session.add(job)

    response = ResponseFactory.build()
    response.job_id = job.id
    response.user_id = mock_user.id
    sa_session.add(response)

    sa_session.flush()

    all_available_responses = await response_query.get_responses_by_job_id(
        db=sa_session, job_id=job.id, user_id=mock_own_company.id
    )
    assert all_available_responses
    assert len(all_available_responses) == 1
    assert all_available_responses[0] == response


@pytest.mark.asyncio
async def test_get_null_responses_by_job_id_for_company(
    sa_session, mock_own_company: User
):
    job = JobFactory.build()
    job.user_id = mock_own_company.id
    sa_session.add(job)
    sa_session.flush()

    non_exist_job = await response_query.get_responses_by_job_id(
        db=sa_session, job_id=job.id, user_id=mock_own_company.id
    )
    assert non_exist_job == []
