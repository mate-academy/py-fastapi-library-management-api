from fastapi import (
    FastAPI,
    Depends,
    HTTPException
)
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from typing import List, Optional

import models
import schemas
import crud
from database import engine, get_db


models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Library Management API")


@app.post("/authors/", response_model=schemas.Author, status_code=201)
def create_author(author: schemas.AuthorCreate, db: Session = Depends(get_db)):
    try:
        return crud.create_author(db=db, author=author)
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=409,
            detail=f"Author with name '{author.name}' already exists"
        )


@app.get("/authors/", response_model=List[schemas.Author])
def read_authors(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    authors = crud.get_authors(db, skip=skip, limit=limit)

    return authors


@app.get("/authors/{author_id}", response_model=schemas.Author)
def read_author(author_id: int, db: Session = Depends(get_db)):
    db_author = crud.get_author(db, author_id=author_id)
    if db_author is None:
        raise HTTPException(status_code=404, detail="Author not found")

    return db_author


@app.post("/authors/{author_id}/books/", response_model=schemas.Book, status_code=201)
def create_book_for_author(
    author_id: int,
    book: schemas.BookCreate,
    db: Session = Depends(get_db)
):
    db_author = crud.get_author(db, author_id=author_id)
    if db_author is None:
        raise HTTPException(status_code=404, detail="Author not found")
    return crud.create_book(db=db, book=book, author_id=author_id)


@app.get("/books/", response_model=List[schemas.Book])
def read_books(
    skip: int = 0,
    limit: int = 100,
    author_id: Optional[int] = None,
    db: Session = Depends(get_db)
):
    books = crud.get_books(db, skip=skip, limit=limit, author_id=author_id)

    return books
