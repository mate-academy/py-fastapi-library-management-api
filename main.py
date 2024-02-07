from database import SessionLocal
from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

import crud
import schemas
from models import Book

app = FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/books/", response_model=list[schemas.Book])
def read_books(
        db: Session = Depends(get_db),
        skip: int = 0,
        limit: int = 100
) -> list[schemas.Book]:
    books = crud.get_all_books(db, skip=skip, limit=limit)
    return books


@app.get("/books/{book_id}/", response_model=schemas.Book)
def read_single_book(
        book_id: int,
        db: Session = Depends(get_db)
) -> schemas.Book:
    db_book = crud.get_book(db, book_id=book_id)
    if db_book is None:
        raise HTTPException(
            status_code=404, detail="Book not found"
        )

    return db_book


@app.post("/books/", response_model=schemas.BookCreate)
def create_book(
        book: schemas.BookCreate,
        db: Session = Depends(get_db)
) -> schemas.BookCreate:
    return crud.create_book(db=db, book=book)


@app.get("/authors/", response_model=list[schemas.Author])
def read_authors(
        db: Session = Depends(get_db),
        skip: int = 0,
        limit: int = 100
) -> list[schemas.Author]:

    return crud.get_all_authors(db, skip=skip, limit=limit)


@app.get("/authors/{author_id}/", response_model=schemas.Author)
def read_book(
        author_id: int,
        db: Session = Depends(get_db)
) -> schemas.Author:
    db_author = crud.get_author(db, author_id=author_id)

    if db_author is None:
        raise HTTPException(
            status_code=404, detail="Author not found"
        )

    return db_author


@app.post("/authors/", response_model=schemas.Author)
def create_author(
        author: schemas.AuthorCreate,
        db: Session = Depends(get_db)
) -> schemas.Author:
    return crud.create_author(db=db, author=author)
