from typing import List

from fastapi import FastAPI
from fastapi.params import Depends, Query
from sqlalchemy.orm import Session

import crud
import schemas
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
    return {"Hello": "World"}


@app.post("/create/author/", response_model=schemas.AuthorCreate)
def create_author(
    author: schemas.AuthorCreate,
    db: Session = Depends(get_db),
):
    return crud.create_author(db=db, author=author)


@app.get("/authors/", response_model=List[schemas.Author])
def read_authors(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=0),
    db: Session = Depends(get_db),
):

    return crud.list_authors(db=db, skip=skip, limit=limit)


@app.get("/author/{author_id}/", response_model=schemas.Author)
def get_author(author_id: int, db: Session = Depends(get_db)):
    return crud.single_author(db=db, author_id=author_id)

@app.post("/book/create/", response_model=schemas.BookCreate)
def create_book(book: schemas.BookCreate, db: Session = Depends(get_db)):
    return crud.create_book(db=db, book=book)


@app.get("/authors/", response_model=List[schemas.Book])
def read_authors(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=0),
    db: Session = Depends(get_db),
):

    return crud.list_books(db=db, skip=skip, limit=limit)

@app.get("/books/{author_id}", response_model=List[schemas.Book])
def read_books_by_author(author_id: int, db: Session = Depends(get_db)):
    return crud.get_books_by_author_id(db=db, author_id=author_id)