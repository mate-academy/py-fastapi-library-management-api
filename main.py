import models

from typing import Annotated

from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

import schemas
from crud import (
    get_all_authors,
    get_author_by_name,
    get_author_by_id,
    get_all_books,
    get_book_by_title,
    create_author,
    create_book,
    get_book_by_id,
)
from database import SessionLocal
from database import Base, engine


Base.metadata.create_all(bind=engine)
app = FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/authors/", response_model=list[schemas.AuthorList])
def read_authors(
        db: Session = Depends(get_db),
        skip: int = 0,
        limit: int = 100
):
    return get_all_authors(db, skip=skip, limit=limit)


@app.post("/authors/", response_model=schemas.AuthorList)
def create_one_author(
    author: schemas.AuthorCreate, db: Annotated[Session, Depends(get_db)]
):
    db_author = get_author_by_name(db=db, name=author.name)
    if db_author:
        raise HTTPException(
            status_code=400, detail="Author with this name already exists"
        )

    return create_author(db=db, author=author)


@app.get("/authors/{author_id}/", response_model=schemas.AuthorList)
def read_single_author(
        author_id: int,
        db: Annotated[Session,
        Depends(get_db)]
):
    db_author = get_author_by_id(db=db, author_id=author_id)

    if not db_author:
        raise HTTPException(status_code=404, detail="Author not found")

    return db_author


@app.get("/books/", response_model=list[schemas.BookList])
def read_books(
    db: Session = Depends(get_db),
    author_id: int | None = None,
    skip: int = 0,
    limit: int = 100,
):
    return get_all_books(db=db, author_id=author_id, skip=skip, limit=limit)


@app.post("/books/", response_model=schemas.BookList)
def create_one_book(
        book: schemas.BookCreate,
        db: Annotated[Session,
        Depends(get_db)]
):
    db_book = get_book_by_title(db=db, title=book.title)
    if db_book:
        raise HTTPException(
            status_code=400, detail="Book with this title already exists"
        )
    book_author = get_author_by_id(db=db, author_id=book.author_id)
    if not book_author:
        raise HTTPException(status_code=400, detail="Author not found")

    return create_book(db=db, book=book)


@app.get("/books/{book_id}/", response_model=schemas.BookList)
def read_single_book(book_id: int, db: Annotated[Session, Depends(get_db)]):
    db_book = get_book_by_id(db=db, book_id=book_id)

    if not db_book:
        raise HTTPException(status_code=404, detail="Book not found")

    return db_book
