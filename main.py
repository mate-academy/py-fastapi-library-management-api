from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

import models
import schemas
import crud
from database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Library Management API")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/authors/", response_model=schemas.AuthorRead)
def create_author(
    author: schemas.AuthorCreate,
    db: Session = Depends(get_db)
):
    return crud.create_author(db, author)


@app.get("/authors/", response_model=List[schemas.AuthorRead])
def read_authors(
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(get_db)
):
    return crud.get_authors(db, skip, limit)


@app.get("/authors/{author_id}", response_model=schemas.AuthorRead)
def read_author(author_id: int, db: Session = Depends(get_db)):
    author = crud.get_author_by_id(db, author_id)
    if not author:
        raise HTTPException(status_code=404, detail="Author not found")
    return author


@app.post("/authors/{author_id}/books/", response_model=schemas.BookRead)
def create_book_for_author(
    author_id: int,
    book: schemas.BookCreate,
    db: Session = Depends(get_db)
):
    author = crud.get_author_by_id(db, author_id)
    if not author:
        raise HTTPException(status_code=404, detail="Author not found")

    return crud.create_book(db, author_id, book)


@app.get("/books/", response_model=List[schemas.BookRead])
def read_books(
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(get_db)
):
    return crud.get_books(db, skip, limit)


@app.get("/books/by-author/{author_id}", response_model=List[schemas.BookRead])
def read_books_by_author(
    author_id: int,
    db: Session = Depends(get_db)
):
    return crud.get_books_by_author(db, author_id)
