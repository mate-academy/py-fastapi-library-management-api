from typing import Type

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

import crud, models, schemas
from database import SessionLocal, engine

from models import Author, Book

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


def get_db() -> None:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/authors/", response_model=schemas.Author)
def create_author(
        author: schemas.AuthorCreate,
        db: Session = Depends(get_db)
) -> Author:
    db_author = crud.get_author_by_name(db, author_name=author.name)
    if db_author:
        raise HTTPException(status_code=400, detail="Author already exists")

    return crud.create_author(db=db, author=author)


@app.get("/authors/", response_model=list[schemas.Author])
def read_authors(
        skip: int = 0,
        limit: int = 10,
        db: Session = Depends(get_db)
) -> list[Type[Author]]:
    authors = crud.get_authors(db, skip=skip, limit=limit)
    return authors


@app.get("/authors/{author_id}/", response_model=schemas.Author)
def read_author(
        author_id: int,
        db: Session = Depends(get_db)
) -> schemas.Author:
    db_author = crud.get_author(db, author_id=author_id)
    if db_author is None:
        raise HTTPException(status_code=404, detail="Author not found")

    return db_author


@app.post("/authors/{author_id}/books/", response_model=schemas.Book)
def create_book_for_author(
        author_id: int,
        book: schemas.BookCreate,
        db: Session = Depends(get_db)
) -> schemas.Book:
    return crud.create_author_book(db=db, book=book, author_id=author_id)


@app.get("/books/", response_model=list[schemas.Book])
def read_books(
        skip: int = 0,
        limit: int = 10,
        db: Session = Depends(get_db)
) -> list[Type[Book]]:
    books = crud.get_books(db, skip=skip, limit=limit)
    return books


@app.get("/books/{book_id}/", response_model=schemas.Book)
def read_book(book_id: int, db: Session = Depends(get_db)) -> Type[Book]:
    db_book = crud.get_book(db, book_id=book_id)
    if db_book is None:
        raise HTTPException(status_code=404, detail="Book not found")

    return db_book
