from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase


DATABASE_URL = "sqlite:///./db/library.db"
engine = create_engine(
    DATABASE_URL, connect_args={"check_same_thread": False}
)


SessionCreator = sessionmaker(autocommit=False, autoflush=False, bind=engine)


class Base(DeclarativeBase):
    pass
