from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

sqlite_file_name = "database.db"
SQLITE_URL = f"sqlite:///{sqlite_file_name}"

connect_args = {"check_same_thread": False}
engine = create_engine(SQLITE_URL, connect_args=connect_args)

SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
)


def get_db():
    with SessionLocal() as db:
        yield db


class Base(DeclarativeBase):
    pass
