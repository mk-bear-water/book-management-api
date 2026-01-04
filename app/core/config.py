from functools import lru_cache
from typing import Literal

from pydantic import computed_field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    ENVIRONMENT: Literal["local", "staging", "production"] = "local"
    PROJECT_NAME: str

    DATABASE_URL: str | None = None

    DATABASE_DIALECT: str = "mysql"
    DATABASE_DRIVER: str = "pymysql"
    DATABASE_HOST: str = "db"
    DATABASE_PORT: int = 3306
    DATABASE_USER: str = "app"
    DATABASE_PASSWORD: str = "app"
    DATABASE_NAME: str = "app"

    @computed_field
    @property
    def database_url(self) -> str:
        if self.DATABASE_URL:
            return self.DATABASE_URL

        scheme = f"{self.DATABASE_DIALECT}+{self.DATABASE_DRIVER}"
        return (
            f"{scheme}://{self.DATABASE_USER}:{self.DATABASE_PASSWORD}"
            f"@{self.DATABASE_HOST}:{self.DATABASE_PORT}/{self.DATABASE_NAME}"
            "?charset=utf8mb4"
        )

    model_config = SettingsConfigDict(
        env_file=".env",
        env_ignore_empty=True,
        extra="ignore",
    )


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
