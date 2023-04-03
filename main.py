from __future__ import annotations
from typing import Union
from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
import crud
import schemas
from database import SessionLocal
from fastapi import FastAPI

app = FastAPI()


class DBSession:
    def __init__(self):
        self._session = None

    def __enter__(self):
        self._session = SessionLocal()
        return self._session

    def __exit__(self, exc_type, exc_value, traceback):
        self._session.close()


def get_db() -> Session:
    with DBSession() as db:
        yield db


@app.get("/")
def root() -> dict:
    return {"message": "Hello World"}


@app.get("/authors/", response_model=list[schemas.Author])
def read_author(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return crud.get_all_author(db=db, skip=skip, limit=limit)


@app.post("/authors/", response_model=schemas.Author)
def create_author(author: schemas.AuthorCreate, db: Session = Depends(get_db)):
    db_author = crud.get_author_by_name(db=db, name=author.name)
    if db_author:
        raise HTTPException(status_code=400, detail="Such author already exists")
    return crud.create_author(db=db, author=author)


@app.get("/authors/{author_id}/", response_model=schemas.Author)
def read_single_author(
    author_id: Union[int, None] = None, db: Session = Depends(get_db)
):
    db_author = crud.get_author(db=db, author_id=author_id)
    if db_author is None:
        raise HTTPException(status_code=404, detail="Author not found")
    return db_author


@app.get("/books/", response_model=list[schemas.Book])
def read_book(
    author_id: int = None, skip: int = 0, limit: int = 10, db: Session = Depends(get_db)
):
    queryset = crud.get_book_list(db=db, author_id=author_id, skip=skip, limit=limit)
    return queryset


@app.post("/books/", response_model=schemas.Book)
def create_book(book: schemas.BookCreate, db: Session = Depends(get_db)):
    return crud.create_book(db=db, book=book)
