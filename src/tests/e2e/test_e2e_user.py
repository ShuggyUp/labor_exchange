import pytest
from fastapi import status
from pydantic import ValidationError
from sqlalchemy.exc import IntegrityError
from fixtures.users import UserFactory
from models import User
from schemas import UserInSchema, UserUpdateSchema


@pytest.mark.asyncio
async def test_create_user(mock_app_unauthorized_user):
    user = UserInSchema(
        name="user",
        email="user@mail.ru",
        password="stringgg",
        password2="stringgg",
        is_company=False,
    )

    registered_user = await mock_app_unauthorized_user.post(
        url="/users", json=user.dict()
    )

    assert registered_user.status_code == status.HTTP_200_OK
    assert registered_user.json()["name"] == user.name


@pytest.mark.asyncio
async def test_create_user_with_email_validation_error(mock_app_unauthorized_user):
    with pytest.raises(ValidationError):
        user = UserInSchema(
            name="user",
            email="user.mail.ru",
            password="stringgg",
            password2="stringgg",
            is_company=False,
        )

        await mock_app_unauthorized_user.post(url="/users", json=user.dict())


@pytest.mark.asyncio
async def test_create_user_with_password_validation_error(mock_app_unauthorized_user):
    with pytest.raises(ValidationError):
        user = UserInSchema(
            name="user",
            email="user@mail.ru",
            password="str",
            password2="str",
            is_company=False,
        )

        await mock_app_unauthorized_user.post(url="/users", json=user.json())


@pytest.mark.asyncio
async def test_create_registered_user(sa_session, mock_app_unauthorized_user):
    with pytest.raises(IntegrityError):
        old_user = UserFactory.build()
        sa_session.add(old_user)
        sa_session.flush()

        new_user = UserInSchema(
            name="user",
            email=old_user.email,
            password="stringgg",
            password2="stringgg",
            is_company=False,
        )

        await mock_app_unauthorized_user.post(url="/users", json=new_user.dict())


@pytest.mark.asyncio
async def test_get_users(mock_app_user):
    users = await mock_app_user.get("/users")

    assert users.status_code == status.HTTP_200_OK


@pytest.mark.asyncio
async def test_update_user(mock_app_user, mock_user: User):
    updated_test_user = UserUpdateSchema(
        name="user2",
    )

    updated_user = await mock_app_user.put(
        url=f"/users?user_id={mock_user.id}", json=updated_test_user.dict()
    )

    assert updated_user.status_code == status.HTTP_200_OK
    assert updated_user.json()["name"] == updated_test_user.name


@pytest.mark.asyncio
async def test_update_user_without_access(sa_session, mock_app_user):
    user = UserFactory.build()
    sa_session.add(user)
    sa_session.flush()

    updated_test_user = UserUpdateSchema(
        name="user2",
    )

    updated_user = await mock_app_user.put(
        url=f"/users?user_id={user.id}", json=updated_test_user.dict()
    )

    assert updated_user.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.asyncio
async def test_update_user_with_same_email(sa_session, mock_app_user, mock_user: User):
    user = UserFactory.build()
    sa_session.add(user)
    sa_session.flush()

    updated_test_user = UserUpdateSchema(
        email=user.email,
    )

    updated_user = await mock_app_user.put(
        url=f"/users?user_id={mock_user.id}", json=updated_test_user.dict()
    )

    assert updated_user.status_code == status.HTTP_409_CONFLICT
