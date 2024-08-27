from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str = "Library API"
    DATABASE_URL: str
    DEFAULT_SKIP_VALUE: int = 0
    DEFAULT_LIMIT_VALUE: int = 3

    class Config:
        env_file = ".env"


settings = Settings()
