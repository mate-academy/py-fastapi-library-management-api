from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from .engine import engine


SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


Base = declarative_base()
