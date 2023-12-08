from datetime import date
from typing import Generator

from fastapi import Depends, FastAPI, HTTPException, status
from sqlalchemy.orm import Session

from db import DBAuthor, DBBook, SessionLocal

from . import crud, schemas

app = FastAPI()


# Dependency.
def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
def root() -> dict:
    return {"message": "Hello World!"}


@app.get("/authors/", response_model=list[schemas.Author])
def read_authors(
    skip: int = 0, limit: int = 100, db: Session = Depends(get_db)
) -> list[DBAuthor]:
    return crud.get_authors(db, skip, limit)


@app.get("/authors/{author_id}/", response_model=schemas.Author | None)
def read_author_by_id(
    author_id: int, db: Session = Depends(get_db)
) -> DBAuthor | None:
    return crud.get_author_by_id(db, author_id)


@app.post("/authors/", response_model=schemas.Author)
def create_author(
    author: schemas.AuthorCreate, db: Session = Depends(get_db)
) -> DBAuthor:
    if crud.get_author_by_name(db, name=author.name):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Author already registered.",
        )
    return crud.create_author(db, author)


@app.get("/books/", response_model=list[schemas.Book])
def read_books(
    skip: int = 0,
    limit: int = 100,
    title: str | None = None,
    summary: str | None = None,
    publication_date: date | None = None,
    db: Session = Depends(get_db),
) -> list[DBBook]:
    return crud.get_books(db, skip, limit, title, summary, publication_date)


@app.get("/books/{author_id}/", response_model=schemas.Book | None)
def read_book_by_author_id(
    author_id: int, db: Session = Depends(get_db)
) -> DBBook | None:
    return crud.get_book_by_id(db, author_id)


@app.post("/books/", response_model=schemas.Book)
def create_book(
    book: schemas.BookCreate, db: Session = Depends(get_db)
) -> DBBook:
    return crud.create_book(db, book)
