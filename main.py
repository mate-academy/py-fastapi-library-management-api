from typing import List

from fastapi import Depends, FastAPI, Query
from sqlalchemy.orm import Session

import crud
import schemas
from db import models
from db.engine import SessionLocal

app = FastAPI()


def get_bd() -> Session:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/authors/")
def all_authors(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, gt=0),
    db: Session = Depends(get_bd),
) -> list[schemas.Author]:
    authors_qs = crud.get_all_authors(db)
    authors = authors_qs.offset(skip).limit(limit).all()
    return authors


@app.post("/authors/", response_model=schemas.Author)
def create_author(
    author: schemas.AuthorCreate,
    db: Session = Depends(get_bd),
) -> schemas.Author:
    return crud.create_author(db, author)


@app.get("/authors/{author_id}/", response_model=schemas.Author)
def get_specific_author(
    author_id: int,
    db: Session = Depends(get_bd),
) -> schemas.Author:
    return crud.get_author(db, author_id)


@app.get("/books/", response_model=List[schemas.Book])
def all_books(
    db: Session = Depends(get_bd),
    skip: int = Query(0, ge=0),
    limit: int = Query(10, gt=0),
    author_id: int = Query(None),
) -> List[schemas.Book]:
    books_qs = crud.get_all_books(db)
    if author_id is not None:
        books_qs = books_qs.filter(models.Book.author_id == author_id)
    books = books_qs.offset(skip).limit(limit).all()
    return books


@app.post("/books/", response_model=schemas.Book)
def create_book(
    book: schemas.BookCreate,
    db: Session = Depends(get_bd),
) -> schemas.Book:
    return crud.create_book(db, book)


@app.get("/books/{books_id}/", response_model=schemas.Book)
def get_specific_book(
    books_id: int,
    db: Session = Depends(get_bd),
) -> schemas.Book:
    return crud.get_book(db, books_id)
