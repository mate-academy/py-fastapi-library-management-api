from typing import Generator, Annotated

from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

import crud
import schemas
from database import SessionLocal, engine, Base

Base.metadata.create_all(bind=engine)

app = FastAPI()

def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

CurrentSession = Annotated[Session, Depends(get_db)]

@app.get("/authors/", response_model=list[schemas.Author])
def get_authors(
        db: CurrentSession,
        skip: int = 0,
        limit: int = 10
) -> list[schemas.Author]:
    return crud.get_all_authors_with_pagination(db, skip, limit)

@app.get("/authors/{author_id}/", response_model=schemas.Author)
def get_author_by_id(
        db: CurrentSession,
        author_id: int
) -> schemas.Author:
    author = crud.get_author_by_id(db, author_id)

    if not author:
        raise HTTPException(status_code=404, detail="Author not found")

    return author

@app.post("/authors/", response_model=schemas.Author)
def create_author(
        db: CurrentSession,
        author: schemas.AuthorCreate
) -> schemas.Author:
    return crud.create_author(db, author)

@app.get("/books/", response_model=list[schemas.Book])
def get_books(
        db: CurrentSession,
        skip: int = 0,
        limit: int = 10,
        author_id: int | None = None
) -> list[schemas.Book]:
    return crud.get_all_books_with_pagination(db, skip, limit, author_id)

@app.post("/books/", response_model=schemas.Book)
def create_book(
        db: CurrentSession,
        book: schemas.BookCreate
) -> schemas.Book:
    return crud.create_book(db, book)
