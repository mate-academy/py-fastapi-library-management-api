from typing import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker

SQLALCHEMY_DATABASE_URL = "sqlite:///./library.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


class Base(DeclarativeBase):
    """Base class for all database models."""


def get_db() -> Generator[Session, None, None]:
    """
    Dependency for database session.

    Returns:
        Session: SQLAlchemy database session
        that will be automatically closed after use.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
