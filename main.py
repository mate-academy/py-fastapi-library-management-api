from __future__ import annotations
from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session

import crud
import schemas
from db.database import SessionLocal

app = FastAPI()


def get_db() -> SessionLocal:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
def root():
    return {"message": "Hallo world"}


@app.get("/books/", response_model=list[schemas.Book])
def books_list(
        skip: int = 0, limit: int = 100,
        db: SessionLocal = Depends(get_db)
):
    return crud.get_all_books(db, skip=skip, limit=limit)


@app.get("/books/{book_id}/", response_model=schemas.Book)
def get_book(book_id: int, db: SessionLocal = Depends(get_db)):
    return crud.get_book(db, book_id=book_id)


@app.get("/books/author/{author_id}/", response_model=list[schemas.Book])
def get_books_by_author(
        author_id: int,
        db: SessionLocal = Depends(get_db)
):
    return crud.filter_books_by_author(db, author_id=author_id)


@app.post("/books/", response_model=schemas.Book)
def create_book(
        book: schemas.BookCreate,
        db: SessionLocal = Depends(get_db)
):
    return crud.create_book(db=db, book=book)


@app.get("/authors/", response_model=list[schemas.Author])
def get_all_authors(
        skip: int = 0, limit: int = 50,
        db: SessionLocal = Depends(get_db)
):
    return crud.get_all_authors(db, skip=skip, limit=limit)


@app.get("/authors/{author_id}/", response_model=schemas.Author)
def get_author(author_id: int, db: SessionLocal = Depends(get_db)):
    return crud.get_author(db, author_id=author_id)


@app.post("/authors/", response_model=schemas.Author)
def create_author(
        author: schemas.AuthorCreate,
        db: SessionLocal = Depends(get_db)
):
    return crud.create_author(db=db, author=author)
