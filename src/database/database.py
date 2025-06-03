"""Database engine and session setup."""

from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from src.config.settings import get_settings

settings = get_settings()

SQLALCHEMY_DATABASE_URL = "sqlite:///./library.db"

# Postgres settings
# SQLALCHEMY_DATABASE_URL = (
#     f'postgresql+asyncpg://{settings.POSTGRES_USER}:{settings.POSTGRES_PASSWORD}'
#     f'@{settings.POSTGRES_HOST}:{settings.POSTGRES_PORT}/{settings.POSTGRES_DB}'
# )

engine = create_async_engine(SQLALCHEMY_DATABASE_URL, echo=True, future=True)

SessionLocal = async_sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False
)


async def get_db():
    """Async DB session generator."""
    async with SessionLocal() as session:
        yield session
