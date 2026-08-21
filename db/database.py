from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = "sqlite:///./py-fastapi-library-management-api.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"autocommit": False, "check_same_thread": False},
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
