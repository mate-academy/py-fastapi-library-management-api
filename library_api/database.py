from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


# connect_args={"check_same_thread": False} is required only for SQLite
SQLALCHEMY_DATABASE_URL = "sqlite:///./library.db"

engine = create_engine(
    # In a real environment, you might change this for other DBs (e.g., PostgreSQL)
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
