from typing import Annotated, Generator

from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from database import SessionLocal

import crud
import schemas
from models import Author, Book

app = FastAPI()


def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()


@app.post(
    "/authors/",
    response_model=schemas.Author,
    status_code=201,
)
def create_author(
        author: schemas.AuthorCreate,
        db: Session = Depends(get_db),
):
    return crud.create_author(db, author)


@app.get(
    "/authors/",
    response_model=list[schemas.Author],
)
def get_authors(
        skip: int = 0,
        limit: int = 100,
        db: Session = Depends(get_db),
):
    return crud.get_all_authors(db, skip, limit)


@app.get(
    "/authors/{author_id}",
    response_model=schemas.Author,
)
def get_author(
        author_id: int,
        db: Session = Depends(get_db),
):
    author = crud.get_author_by_id(db, author_id)

    if author is None:
        raise HTTPException(
            status_code=404,
            detail="Author not found",
        )

    return author


@app.post(
    "/authors/{author_id}/books/",
    response_model=schemas.Book,
    status_code=201,
)
def create_book(
        author_id: int,
        book: schemas.BookCreate,
        db: Session = Depends(get_db),
):
    author = crud.get_author_by_id(db, author_id)

    if author is None:
        raise HTTPException(
            status_code=404,
            detail="Author not found",
        )

    book.author_id = author_id

    return crud.create_book(db, book)


@app.get(
    "/books/",
    response_model=list[schemas.Book],
)
def get_books(
        skip: int = 0,
        limit: int = 100,
        author_id: int | None = None,
        db: Session = Depends(get_db),
):
    return crud.get_all_books(
        db=db,
        skip=skip,
        limit=limit,
        author_id=author_id,
    )
