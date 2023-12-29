from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional

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
def read_authors(
        skip: int = 0,
        limit: int = 2,
        db: Session = Depends(get_db)
) -> List[schemas.Author]:
    return crud.get_all_authors(db, skip=skip, limit=limit)


@app.get("/authors/{author_id}/", response_model=schemas.Author)
def read_single_author(author_id: int, db: Session = Depends(get_db)) -> schemas.Author:
    db_author = crud.get_author(db=db, author_id=author_id)

    if db_author is None:
        raise HTTPException(status_code=404, detail="Author is not found")

    return db_author


@app.post("/authors/", response_model=schemas.Author)
def create_author(
        author: schemas.AuthorCreate,
        db: Session = Depends(get_db)
) -> schemas.Author:
    db_author = crud.get_author(db=db, author_id=author.id)

    if db_author:
        raise HTTPException(
            status_code=400,
            detail="Author is already exist"
        )
    return crud.create_author(db=db, author=author)


@app.get("/books/", response_model=list[schemas.Book])
def read_books(
        skip: int = 0,
        limit: int = 2,
        author_id: int | None = None,
        db: Session = Depends(get_db)
               ) -> List[schemas.Book]:
    return (
        crud.get_all_books(db=db, author_id=author_id, skip=skip, limit=limit)
    )


@app.get("/books/{book_id}/", response_model=schemas.Book)
def read_single_book(book_id: int, db: Session = Depends(get_db)) -> schemas.Book:
    db_book = crud.get_book(db=db, book_id=book_id)

    if db_book is None:
        raise HTTPException(status_code=404, detail="Book is not found")

    return db_book


@app.post("/books/", response_model=schemas.Book)
def create_book(book: schemas.BookCreate, db: Session = Depends(get_db)) -> schemas.Book:
    return crud.create_book(db=db, book=book)
