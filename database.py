from typing import Any, Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

DB_URL = "sqlite:///./book_library.db"


engine = create_engine(DB_URL, echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def create_db_session() -> Generator[Session, Any, None]:
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()
