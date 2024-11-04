from typing import Optional

from fastapi import FastAPI, Depends, HTTPException
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


@app.get("/authors/", response_model=list[schemas.Author])
def read_authors(
    skip: Optional[int],
    limit: Optional[int],
    db: Session = Depends(get_db)):
    return crud.get_all_authors(db, skip, limit)


@app.get("/authors/{author_id}/", response_model=schemas.Author)
def read_author_by_id(
    author_id: int,
    db: Session = Depends(get_db),
):
    return crud.get_author(db, author_id)


@app.post("/authors/", response_model=schemas.Author)
def create_author(
    author: schemas.AuthorCreate,
    db: Session = Depends(get_db),
):
    db_author = crud.get_author_by_name(db, author.name)
    if db_author:
        raise HTTPException(
            status_code=400,
            detail=f"Such author with name '{author.name}' already exists."
        )

    return crud.create_author(db, author)


@app.get("/books/", response_model=list[schemas.Book])
def read_books(
    skip: Optional[int],
    limit: Optional[int],
    author_id: Optional[int],
    db: Session = Depends(get_db),
):
    return crud.get_all_books(db, author_id, skip, limit)


@app.post("/books/", response_model=schemas.Book)
def create_book(
    book: schemas.BookCreate,
    db: Session = Depends(get_db),
):
    db_book = crud.get_book_by_title(db, book.title)
    if db_book:
        raise HTTPException(
            status_code=400,
            detail=f"Such book with title '{book.title}' already exists."
        )

    return crud.create_book(db, book)
