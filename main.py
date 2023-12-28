from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session

from typing import Union

import schemas
import crud
from database import SessionLocal


app = FastAPI()


def get_db() -> Session:
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()


@app.get("/")
def read_root():
    return "Hello World"


@app.get("/authors/", response_model=list[schemas.Author])
def read_author_list(db: Session = Depends(get_db)):
    return crud.get_author_list(db)


@app.post("/authors/", response_class=schemas.Author)
def create_author(author: schemas.AuthorCreate,
                  db: Session = Depends(get_db)):
    return crud.create_author(author=author, db=db)