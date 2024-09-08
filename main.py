from fastapi import FastAPI, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from typing import List
from sqlalchemy.exc import IntegrityError

import models
from database import SessionLocal
import schema
import crud


def get_db() -> Session:
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()


class PaginationParams:
    def __init__(self, skip: int = Query(0, ge=0), limit: int = Query(10, ge=1)):
        self.skip = skip
        self.limit = limit


app = FastAPI()


@app.get("/authors/", response_model=List[schema.Author])
def read_authors(
        pagination: PaginationParams = Depends(),
        db: Session = Depends(get_db)
) -> List[schema.Author]:
    return crud.get_all_authors(db, skip=pagination.skip, limit=pagination.limit)


@app.get("/author/{author_id}/", response_model=schema.Author)
def read_author(
        author_id: int, db: Session = Depends(get_db)
) -> schema.Author:
    db_author = crud.get_author_by_id(db, author_id)
    if db_author is None:
        raise HTTPException(status_code=404, detail="Author not found")
    return db_author


@app.post("/authors/", response_model=schema.Author)
def create_author(
        author: schema.AuthorCreate,
        db: Session = Depends(get_db)
) -> schema.Author:
    db_author = crud.get_author_by_id(db, author.id)
    if db_author:
        raise HTTPException(status_code=409, detail="Author already exists")
    return crud.create_new_author(db, author=author)


@app.get("/books/", response_model=List[schema.Book])
def read_books(
        pagination: PaginationParams = Depends(),
        db: Session = Depends(get_db)
) -> List[schema.Book]:
    return crud.get_all_books(db, skip=pagination.skip, limit=pagination.limit)


@app.post("/books/", response_model=schema.Book)
def create_book(
        book: schema.BookCreate,
        db: Session = Depends(get_db)
) -> schema.Book:
    existing_book = db.query(models.Book).filter(models.Book.title == book.title).first()
    if existing_book:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Book with this title already exists."
        )

    try:
        new_book = crud.create_new_book(db, book=book)
        return new_book
    except IntegrityError:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while creating the book."
        )
