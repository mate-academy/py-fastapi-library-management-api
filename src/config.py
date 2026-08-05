from functools import lru_cache

from pydantic import PostgresDsn, computed_field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    POSTGRES_DB: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_HOST: str
    POSTGRES_PORT: int
    POSTGRES_DRIVER: str

    model_config = SettingsConfigDict(
        env_file=[".env", "../.env"], env_file_encoding="utf-8", extra="ignore"
    )

    @computed_field
    def construct_db_url(self) -> str:
        return PostgresDsn.build(
            scheme=f"{self.POSTGRES_DRIVER}",
            username=f"{self.POSTGRES_USER}",
            password=f"{self.POSTGRES_PASSWORD}",
            host=f"{self.POSTGRES_HOST}",
            port=self.POSTGRES_PORT,
        ).unicode_string()


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
