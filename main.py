from typing import Type

from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

import crud
import schemas
from database import SessionLocal
from models import Author, Book

app = FastAPI()


def get_db() -> Session:
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()


@app.get("/authors/", response_model=list[schemas.Author])
def read_authors(
        skip: int = 0,
        limit: int = 100,
        db: Session = Depends(get_db)
) -> list[Type[Author]]:
    authors = crud.get_authors_list(db=db, skip=skip, limit=limit)
    return authors


@app.post("/authors/", response_model=schemas.Author)
def create_authors(author: schemas.AuthorCreate, db: Session = Depends(get_db)):
    new_author = crud.create_author(db=db, author=author)
    return new_author


@app.get("/authors/{author_id}", response_model=schemas.Author)
def read_single_author(author_id: int, db: Session = Depends(get_db)):
    author = crud.get_author(db, author_id=author_id)
    if author is None:
        raise HTTPException(status_code=404, detail="Author not found")
    return author


@app.get("/books/", response_model=list[Type[schemas.Book]])
def read_books(
        skip: int = 0,
        limit: int = 100,
        db: Session = Depends(get_db)
) -> list[Type[schemas.Book]]:
    books = crud.get_books_list(db=db, limit=limit, skip=skip)
    return books


@app.get("/authors/{author_id}/books", response_model=list[Type[schemas.Book]])
def get_books_by_author(
    author_id: int,
    db: Session = Depends(get_db)
) -> list[Type[schemas.Book]]:
    books = crud.get_books_by_author(db=db, author_id=author_id)
    return books


@app.post("/authors/{authors_id}/books", response_model=schemas.Book)
def create_book_endpoint(
    author_id: int,
    book: schemas.BookCreate,
    db: Session = Depends(get_db)
) -> Book:
    author = crud.get_author(db=db, author_id=author_id)
    if not author:
        raise HTTPException(status_code=404, detail="Not found")
    new_book = crud.create_book(db=db, book=book, author_id=author_id)
    return new_book
