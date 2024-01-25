from pydantic import BaseSettings, Field, validator


class DatabaseSettings(BaseSettings):
    """
    Настройки базы данных
    """

    db_host: str = Field(default="localhost", env="DB_HOST")
    db_port: str = Field(default="5432", env="DB_PORT")
    db_name: str = Field(default="postgres", env="DB_NAME")
    db_user: str = Field(default="postgres", env="DB_USER")
    db_pass: str = Field(env="DB_PASS")

    db_url: str = Field(default=None)

    @validator("db_url")
    def set_db_url(cls, v, values, **kwargs):
        return f"postgresql+asyncpg://{values['db_user']}:{values['db_pass']}@{values['db_host']}:{values['db_port']}/{values['db_name']}"

    class Config:
        env_file = ".env"


class TestDatabaseSettings(BaseSettings):
    """
    Настройки тестовой базы данных
    """

    db_host: str = Field(default="localhost", env="TEST_DB_HOST")
    db_port: str = Field(default="5432", env="TEST_DB_PORT")
    db_name: str = Field(default="postgres", env="TEST_DB_NAME")
    db_user: str = Field(default="postgres", env="TEST_DB_USER")
    db_pass: str = Field(env="TEST_DB_PASS")

    db_url: str = Field(default=None)

    @validator("db_url")
    def set_db_url(cls, v, values, **kwargs):
        return f"postgresql+asyncpg://{values['db_user']}:{values['db_pass']}@{values['db_host']}:{values['db_port']}/{values['db_name']}"

    class Config:
        env_file = ".env"


class UvicornSettings(BaseSettings):
    """
    Настройки сервера
    """

    host: str = Field(default="127.0.0.1", env="SERVER_HOST")
    port: int = Field(default=8000, env="SERVER_PORT")

    class Config:
        env_file = ".env"


class TokenSettings(BaseSettings):
    """
    Настройки токенов
    """

    access_token_expire_minutes: int = Field(
        default=60, env="ACCESS_TOKEN_EXPIRE_MINUTES"
    )
    refresh_token_expire_minutes: int = Field(
        default=120, env="REFRESH_TOKEN_EXPIRE_MINUTES"
    )
    algorithm: str = Field(env="ALGORITHM")
    secret_key: str = Field(env="SECRET_KEY")

    class Config:
        env_file = ".env"


class ProjectSettings(BaseSettings):
    """
    Настройка состояния проекта
    """

    stage: str = Field(default="prod", env="STAGE")

    class Config:
        env_file = ".env"


db_settings = DatabaseSettings()
test_db_settings = TestDatabaseSettings()
server_settings = UvicornSettings()
token_settings = TokenSettings()
project_settings = ProjectSettings()
