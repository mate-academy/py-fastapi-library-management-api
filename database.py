from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URI = "sqlite:///./database.db"

engine = create_engine(SQLALCHEMY_DATABASE_URI)

SessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=engine
)
