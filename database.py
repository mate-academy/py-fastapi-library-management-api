from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.engine import create_engine


SQLALCHEMY_DB_URL = "sqlite:///./library.db"

engine = create_engine(
    SQLALCHEMY_DB_URL,
    connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
