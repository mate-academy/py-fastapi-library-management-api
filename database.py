from typing import Iterator

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

sqlite_file_name = "library.db"
sqlite_url = f"sqlite:///./{sqlite_file_name}"

connect_args = {"check_same_thread": False}
engine = create_engine(sqlite_url, connect_args=connect_args)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db() -> Iterator[Session] | None:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
