from typing import List

from fastapi import FastAPI, Depends, HTTPException, Query
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


@app.get("/books/", response_model=List[schemas.Book])
def get_books(
        db: Session = Depends(get_db),
        author_id: int | None = None,
        skip: int = Query(0, ge=0,
                          description="Number of records to skip"),
        limit: int = Query(10, ge=1, le=100,
                           description="Max records to return"),
):
    return crud.get_all_books(db=db, author_id=author_id,
                              skip=skip, limit=limit)


@app.post("/books/", response_model=schemas.Book)
def create_book(
        book: schemas.BookCreate,
        db: Session = Depends(get_db)
):
    return crud.create_book(db=db, book=book)


@app.get("/books/{book_id}", response_model=schemas.Book)
def get_book(
        book_id: int,
        db: Session = Depends(get_db)
):
    db_book = crud.get_one_book(db=db, book_id=book_id)

    if db_book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    return db_book


@app.get("/authors/", response_model=List[schemas.Author])
def get_authors(
        db: Session = Depends(get_db),
        skip: int = Query(0, ge=0,
                          description="Number of records to skip"),
        limit: int = Query(10, ge=1, le=100,
                           description="Max records to return"),
):
    return crud.get_all_authors(db=db, skip=skip, limit=limit)


@app.get("/authors/{author_id}", response_model=schemas.Author)
def get_author(
    author_id: int,
    db: Session = Depends(get_db)
):
    db_author = crud.get_one_author(db=db, author_id=author_id)
    return db_author


@app.post("/authors/", response_model=schemas.Author)
def create_author(
        author: schemas.AuthorCreate,
        db: Session = Depends(get_db)
):
    db_author = crud.get_author_by_name(db=db, name=author.name)
    if db_author:
        raise HTTPException(
            status_code=400,
            detail="Author with such name already exists"
        )
    return crud.create_author(db=db, author=author)
