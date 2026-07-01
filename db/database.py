from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from db.models import BaseModel

SQLITE_URL = 'sqlite:///./library.db'

engine = create_engine(SQLITE_URL)
SessionLocal = sessionmaker(bind=engine)


def init_db():
    BaseModel.metadata.create_all(engine)
