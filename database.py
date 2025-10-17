import os
from pathlib import Path
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# prefer env var, otherwise use a file-based sqlite URL (Path -> str)
DATABASE_URL = os.getenv(
    "DATABASE_URL", f"sqlite:///{str(Path(__file__).parent / 'app.db')}"
)

# only pass check_same_thread for sqlite URLs
_is_sqlite = DATABASE_URL.startswith("sqlite")
_connect_args = {"check_same_thread": False} if _is_sqlite else {}

engine = create_engine(DATABASE_URL, connect_args=_connect_args)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# centralized declarative base for all models
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()