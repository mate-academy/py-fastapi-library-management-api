from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker


SQLALCHEMY_DATABASE_URL = "sqlite+aiosqlite:///./library.db"


engine = create_async_engine(
    SQLALCHEMY_DATABASE_URL, echo=True, future=True, connect_args={"check_same_thread": False}
)


SessionLocal = async_sessionmaker(
    engine, expire_on_commit=False, autocommit=False, autoflush=False,future=True
)


async def get_db():
    async with SessionLocal() as session:
        yield session
