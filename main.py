from typing import List

from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

import crud
import schemas
from database import SessionLocal

app = FastAPI()


def get_db() -> Session:
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()


@app.get("/authors/", response_model=List[schemas.AuthorList])
def get_all_authors(
        skip: int = 0,
        limit: int = 10,
        db: Session = Depends(get_db)
) -> schemas.AuthorList:
    return crud.get_all_authors(db=db, skip=skip, limit=limit)


@app.get("/authors/{author_id}/", response_model=schemas.AuthorList)
def get_all_authors(
        author_id: int,
        db: Session = Depends(get_db)
) -> schemas.AuthorList:
    author = crud.get_author_by_id(db=db, author_id=author_id)
    if author is None:
        raise HTTPException(status_code=404, detail="Author not found")
    return author


@app.post("/create_author/", response_model=schemas.AuthorList)
def create_author(
        author: schemas.AuthorCreate,
        db: Session = Depends(get_db)
) -> schemas.AuthorList:
    return crud.create_author(db=db, author=author)


@app.get("/books/", response_model=List[schemas.BookList])
def get_all_books(
        skip: int = 0,
        limit: int = 10,
        db: Session = Depends(get_db)
) -> schemas.BookList:
    return crud.get_all_books(db=db, skip=skip, limit=limit)


@app.get("/books/{author_id}", response_model=List[schemas.BookList])
def get_books_by_author_id(
        author_id: int,
        db: Session = Depends(get_db)
) -> schemas.BookList:
    books = crud.get_book_by_author_id(db=db, author_id=author_id)
    if books is None:
        raise HTTPException(status_code=404, detail="Books not found")
    return books


@app.post("/create_book/", response_model=schemas.BookList)
def create_book(
        book: schemas.BookCreate,
        db: Session = Depends(get_db)
) -> schemas.BookList:
    return crud.create_book(db=db, book=book)
