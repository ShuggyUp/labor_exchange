from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session
from config import db_settings, test_db_settings, project_settings


if project_settings.stage == "test":
    SQLALCHEMY_DATABASE_URL = test_db_settings.db_url
else:
    SQLALCHEMY_DATABASE_URL = db_settings.db_url

engine = create_async_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = scoped_session(
    sessionmaker(autocommit=False, autoflush=False, bind=engine, class_=AsyncSession)
)

Base = declarative_base()
