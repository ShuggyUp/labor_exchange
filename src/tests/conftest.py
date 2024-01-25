import asyncio

from sqlalchemy import inspect
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from models import User
from fixtures.users import UserFactory
from fixtures.jobs import JobFactory
from fixtures.responses import ResponseFactory
from fastapi.testclient import TestClient
from main import app
import pytest
import pytest_asyncio
from unittest.mock import MagicMock
from db_connection import SQLALCHEMY_DATABASE_URL
from schemas import AccessTokenSchema
from core.security import create_token
from dependencies import get_db
from httpx import AsyncClient


@pytest.fixture()
def client_app():
    client = TestClient(app)
    return client


@pytest_asyncio.fixture()
async def sa_session():
    engine = create_async_engine(
        SQLALCHEMY_DATABASE_URL
    )  # You must provide your database URL.
    connection = await engine.connect()
    trans = await connection.begin()

    Session = sessionmaker(connection, expire_on_commit=False, class_=AsyncSession)
    session = Session()
    deletion = session.delete

    async def mock_delete(instance):
        inspected = inspect(instance)
        if not inspected.persistent:
            session.expunge(instance)
        else:
            await deletion(instance)

        return await asyncio.sleep(0)

    session.commit = MagicMock(side_effect=session.flush)
    session.delete = MagicMock(side_effect=mock_delete)

    try:
        yield session
    finally:
        await session.close()
        await trans.rollback()
        await connection.close()
        await engine.dispose()


# регистрация фабрик
@pytest_asyncio.fixture(autouse=True)
def setup_factories(sa_session: AsyncSession) -> None:
    UserFactory.session = sa_session
    JobFactory.session = sa_session
    ResponseFactory.session = sa_session


@pytest_asyncio.fixture()
async def mock_user(sa_session: AsyncSession) -> User:
    new_user = UserFactory.build()
    new_user.is_company = False
    sa_session.add(new_user)

    await sa_session.commit()
    await sa_session.refresh(new_user)
    return new_user


@pytest_asyncio.fixture()
async def mock_own_company(sa_session: AsyncSession) -> User:
    new_user = UserFactory.build()
    new_user.is_company = True
    sa_session.add(new_user)

    await sa_session.commit()
    await sa_session.refresh(new_user)
    return new_user


@pytest_asyncio.fixture()
async def mock_another_company(sa_session: AsyncSession) -> User:
    new_user = UserFactory.build()
    new_user.is_company = True
    sa_session.add(new_user)

    await sa_session.commit()
    await sa_session.refresh(new_user)
    return new_user


@pytest_asyncio.fixture()
async def mock_access_token_user(mock_user: User):
    token = AccessTokenSchema(
        access_token=create_token({"sub": mock_user.email}), token_type="Bearer"
    )
    return token


@pytest_asyncio.fixture()
async def mock_access_token_company(mock_own_company: User):
    token = AccessTokenSchema(
        access_token=create_token({"sub": mock_own_company.email}),
        token_type="Bearer",
    )
    return token


@pytest_asyncio.fixture()
async def mock_app_user(sa_session, mock_access_token_user: AccessTokenSchema):
    app.dependency_overrides[get_db] = lambda: sa_session

    async with AsyncClient(app=app, base_url="http://test") as client:
        client.headers[
            "Authorization"
        ] = f"Bearer {mock_access_token_user.access_token}"
        yield client


@pytest_asyncio.fixture()
async def mock_app_company(sa_session, mock_access_token_company: AccessTokenSchema):
    app.dependency_overrides[get_db] = lambda: sa_session

    async with AsyncClient(app=app, base_url="http://test") as client:
        client.headers[
            "Authorization"
        ] = f"Bearer {mock_access_token_company.access_token}"
        yield client


@pytest_asyncio.fixture()
async def mock_app_unauthorized_user(sa_session):
    app.dependency_overrides[get_db] = lambda: sa_session

    async with AsyncClient(app=app, base_url="http://test") as client:
        yield client
