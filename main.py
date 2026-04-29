from typing import Generator, Annotated

from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

import crud
import schemas
import models
from database import SessionLocal, engine, Base

Base.metadata.create_all(bind=engine)

app = FastAPI()


def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/authors/", response_model=list[schemas.Author])
def read_authors(
    db: Annotated[Session, Depends(get_db)],
    skip: int = 0,
    limit: int = 5,
):
    return crud.get_authors_list(db=db, skip=skip, limit=limit)


@app.post("/authors/", response_model=schemas.Author)
def create_author(
    db: Annotated[Session, Depends(get_db)],
    author: schemas.AuthorCreate,
):
    db_author = crud.get_author_by_name(db=db, name=author.name)
    if db_author:
        raise HTTPException(status_code=400, detail="Author already exists")

    return crud.create_author(db=db, author=author)


@app.get("/authors/{author_id}", response_model=schemas.Author)
def read_single_author(
    db: Annotated[Session, Depends(get_db)],
    author_id: int,
):
    db_author = crud.get_author_by_id(db=db, author_id=author_id)

    if not db_author:
        raise HTTPException(status_code=404, detail="Author not found")

    return db_author


@app.post("/books/", response_model=schemas.Book)
def create_book(
    db: Annotated[Session, Depends(get_db)],
        book: schemas.BookCreate,
):
    db_book = crud.get_book_by_title(db=db, title=book.title)
    if db_book:
        raise HTTPException(status_code=400, detail="Book already exists")

    author = crud.get_author_by_id(db=db, author_id=book.author_id)
    if not author:
        raise HTTPException(status_code=404, detail="Author not found")

    return crud.create_book(db=db, book=book)


@app.get("/books/", response_model=list[schemas.Book])
def read_books(
    db: Annotated[Session, Depends(get_db)],
    skip: int = 0,
    limit: int = 5,
    author_id: int | None = None,
):
    return crud.get_books_list(db=db, skip=skip, limit=limit, author_id=author_id)


@app.get("/books/{book_id}", response_model=schemas.Book)
def read_single_book(
        book_id: int,
        db: Annotated[Session, Depends(get_db)],
):
    db_book = crud.get_book_by_id(db=db, book_id=book_id)

    if not db_book:
        raise HTTPException(status_code=404, detail="Book not found")

    return db_book
