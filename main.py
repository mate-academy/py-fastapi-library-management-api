from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session

import crud
from database import SessionLocal
from models import Author, Book
from schemas import (
    AuthorCreateUpdateSchema,
    AuthorListSchema,
    AuthorDetailSchema,
    BookListSchema,
    BookCreateUpdateSchema
)

app = FastAPI()


@app.get("/")
def root():
    return {"message": "Hello World"}


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/authors/", response_model=AuthorListSchema)
def create_new_author(
    author: AuthorCreateUpdateSchema,
    db: Session = Depends(get_db),
) -> Author:
    return crud.create_author(db, author)


@app.get("/authors/", response_model=list[AuthorListSchema])
def read_authors(db: Session = Depends(get_db)) -> list[Author]:
    return crud.read_authors_list(db)


@app.get("/authors/{id}", response_model=AuthorDetailSchema)
def read_author(id: int, db: Session = Depends(get_db)) -> Author:
    return crud.read_author_detail(db, id)


@app.post("/books/", response_model=BookListSchema)
def create_new_book(
        book: BookCreateUpdateSchema,
        db: Session = Depends(get_db)
) -> Book:
    return crud.create_book(db, book)


@app.post("/books/", response_model=BookListSchema)
def read_books(
    author_id: int = None,
    db: Session = Depends(get_db)
) -> list[Book]:
    return crud.read_books_list(db, author_id)
