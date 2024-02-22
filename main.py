from typing import Union

from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

import schemas
import crud
from db.database import SessionLocal

app = FastAPI()


def get_db() -> Session:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
def read_root() -> dict:
    return {"Hello": "World"}


@app.get("/authors/", response_model=list[schemas.Author])
def get_all_authors(db: Session = Depends(get_db)):
    return crud.get_all_authors(db)


@app.post("/authors/", response_model=schemas.Author)
def create_author(author: schemas.AuthorCreate, db: Session = Depends(get_db)):
    db_author = crud.get_author_by_name(db, author.name)
    if db_author:
        raise HTTPException(
            status_code=400,
            detail="Author with such name already exists"
        )

    return crud.create_author(db, author)