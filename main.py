from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

from fastapi import FastAPI

import models
import schemas
import crud
from database import SessionLocal

app = FastAPI()


def get_db() -> Session:
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()


@app.get("/authors/", response_model=list[schemas.Author])
def read_authors(db: Session = Depends(get_db), skip: int = 0, limit: int = 100):
    return crud.get_authors(db=db, skip=skip, limit=limit)


@app.post("/authors/", response_model=schemas.AuthorCreate)
def create_author(
    author: schemas.AuthorCreate,
    db: Session = Depends(get_db),
):
    db_author = crud.create_author(db=db, author=author)
    return db_author


@app.get("/authors/{author_id}/", response_model=schemas.Author)
def read_author_by_id(author_id: int, db: Session = Depends(get_db)):
    db_author = crud.get_author(db=db, author_id=author_id)
    if db_author is None:
        raise HTTPException(
            status_code=400,
            detail="There is no such author"
        )
    return db_author


@app.get("/books/", response_model=list[schemas.Book])
def read_books(db: Session = Depends(get_db), skip: int = 0, limit: int = 100):
    return crud.get_books(db=db, skip=skip, limit=limit)


@app.get("/authors/{author_id}/book/", response_model=list[schemas.Book])
def read_books_by_authors_id(author_id: int, db: Session = Depends(get_db), skip: int = 0, limit: int = 100):
    db_author = crud.get_author(db=db, author_id=author_id)
    if db_author is None:
        raise HTTPException(
            status_code=400,
            detail="There is no such author"
        )

    db_book = crud.get_books_by_authors_id(db, author_id, skip, limit)
    return db_book


@app.post("/authors/{author_id}/book/", response_model=schemas.BookCreate)
def create_book(
    book: schemas.BookCreate,
    author_id: int,
    db: Session = Depends(get_db),
):
    db_author = crud.get_author(db, author_id)
    if db_author is None:
        raise HTTPException(
            status_code=400,
            detail="There is no such author"
        )

    db_book = crud.create_book(db, book)
    return db_book
