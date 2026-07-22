from typing import Annotated

from fastapi import Depends
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session

SQLITE_URL = "sqlite:///./db.sqlite3"

engine = create_engine(SQLITE_URL)

Base = declarative_base()


def get_session():
    with Session(engine) as session:
        yield session


SessionDep = Annotated[Session, Depends(get_session)]
