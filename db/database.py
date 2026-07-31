from sqlalchemy import create_engine
from sqlalchemy.ext import declarative
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = "sqlite:///./library.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
)
# базовий клас за доп. якого будуть створюватися сесії до бд
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
# базовий клас для всіх моделей
Base = declarative.declarative_base()