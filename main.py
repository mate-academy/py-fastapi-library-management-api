from typing import List

from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session

import crud
import schemas
from database import SessionLocal


def get_db() -> Session:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


app = FastAPI()


@app.post("/authors/", response_model=schemas.Author)
def create_author(
        author: schemas.AuthorCreate,
        db: Session = Depends(get_db)
) -> List[schemas.Author]:
    return crud.create_author(db=db, author=author)


@app.get("/authors/", response_model=List[schemas.Author])
def read_authors(
        skip: int = 0,
        limit: int = 10,
        db: Session = Depends(get_db)
) -> List[schemas.Author]:
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
    return crud.create_book(db=db, book=book, author_id=author_id)


@app.get("/books/", response_model=List[schemas.Book])
def read_books(
        skip: int = 0,
        limit: int = 10,
        db: Session = Depends(get_db)
) -> List[schemas.Book]:
    books = crud.get_books(db, skip=skip, limit=limit)
    return books


@app.get(
    "/authors/{author_id}/books/",
    response_model=List[schemas.Book]
)
def read_books_by_author(
        author_id: int,
        skip: int = 0,
        limit: int = 10,
        db: Session = Depends(get_db)
) -> List[schemas.Book]:
    books = crud.get_books_by_author(
        db,
        author_id=author_id,
        skip=skip,
        limit=limit
    )
    return books
