# database.py
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

# 1. Define your SQLite URL (e.g., "sqlite:///./library.db")
SQLALCHEMY_DATABASE_URL = "sqlite:///./library.db"

# 2. Create the engine (Don't forget the check_same_thread argument!)
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})

# 3. Create the SessionLocal class
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 4. Create the Base class for your models
Base = declarative_base()