from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, \
    AsyncSession

DATABASE_URL = "sqlite+aiosqlite:///./lib.db"

async_engine = create_async_engine(DATABASE_URL)
async_session_maker = async_sessionmaker(
    async_engine, expire_on_commit=False
)


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        try:
            yield session
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()
