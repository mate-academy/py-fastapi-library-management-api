from typing import List

from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

import crud
import schemas
from db.database import SessionLocal


app = FastAPI()


def get_db() -> Session:
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()


@app.get("/authors/", response_model=List[schemas.Author])
def read_all_authors(
        db: Session = Depends(get_db),
        skip: int = 0,
        limit: int = 10
) -> List[schemas.Author]:
    return crud.authors_list(db=db, skip=skip, limit=limit)


@app.get("/authors/{author_id}/", response_model=schemas.Author)
def get_author_by_id(
        author_id: int,
        db: Session = Depends(get_db)
) -> schemas.Author:
    db_author = crud.get_author_by_id(
        db=db, author_id=author_id
    )
    if not db_author:
        raise HTTPException(status_code=404, detail="Author not found")
    return db_author


@app.post("/authors/", response_model=schemas.AuthorCreate)
def create_author(
    author: schemas.AuthorCreate,
    db: Session = Depends(get_db),
):
    return crud.create_author(db=db, author=author)


@app.get("/books/", response_model=List[schemas.Book])
def get_books(
        db: Session = Depends(get_db),
        skip: int = 0,
        limit: int = 10
):
    return crud.books_list(db=db, skip=skip, limit=limit)


@app.get("/books/{author_id}/", response_model=schemas.Book)
def get_book_by_id(db: Session = Depends(get_db), author_id: int | None = None) -> schemas.Book:
    db_books = crud.get_book_by_author_id(db=db, author_id=author_id)
    if not db_books:
        raise HTTPException(status_code=404, detail="Author not found")
    return db_books


@app.post("/books/", response_model=schemas.BookCreate)
def create_book(
    book: schemas.BookCreate,
    author_id: int,
    db: Session = Depends(get_db),
):
    author = crud.get_author_by_id(db=db, author_id=author_id)
    if not author:
        raise HTTPException(status_code=404, detail="Author not found")
    return crud.create_book(db=db, book=book, author_id=author_id)
