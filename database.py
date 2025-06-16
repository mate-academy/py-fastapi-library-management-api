from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlmodel import Session

SQLALCHEMY_DATABASE_URL = 'sqlite:///./library.db'

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    echo=True,
    connect_args={'check_same_thread': False}
)

SessionLocal = sessionmaker(
    autocommit=False,
    class_=Session,
    autoflush=False,
    bind=engine
)
