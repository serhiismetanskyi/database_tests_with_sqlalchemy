from functools import cached_property
from pathlib import Path

from pydantic import model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing_extensions import Self


class DB(BaseSettings):
    model_config = SettingsConfigDict(
        extra="ignore",
        env_prefix="postgres_",
        env_file=".env",
        env_file_encoding="utf-8",
    )

    username: str | None = None
    user: str | None = None

    database: str | None = None
    db: str | None = None

    password: str
    host: str
    port: int

    @cached_property
    def uri(self) -> str:
        user = self.username
        password = self.password
        host = self.host
        port = self.port
        db = self.database
        return f"postgresql://{user}:{password}@{host}:{port}/{db}"

    @model_validator(mode="after")
    def check_username_is_set(self) -> Self:
        if self.username is None and self.user is None:
            raise ValueError("postgres_user or postgres_username must be set.")
        if self.username is None:
            self.username = self.user
        return self

    @model_validator(mode="after")
    def check_database_is_set(self) -> Self:
        if self.database is None and self.db is None:
            raise ValueError("postgres_database or postgres_db must be set.")
        if self.database is None:
            self.database = self.db
        return self


class Log(BaseSettings):
    model_config = SettingsConfigDict(
        extra="ignore",
        env_file=".env",
        env_file_encoding="utf-8",
        env_prefix="log_",
    )

    level: str
    config_file_name: str = "logger.ini"
    logger_name: str = "database_tests"


class Settings(BaseSettings):
    db: DB = DB()
    log: Log = Log()

    root_path: str = str(Path(__file__).resolve().parent)


settings: Settings = Settings()