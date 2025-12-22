from fastapi import FastAPI, Depends
from sqlalchemy.orm.session import Session

import crud
import models
from crud import get_author
from database import SessionLocal
from models import Book, Author
from schemas import BookRead, AuthorRead, AuthorCreate, BookCreate

app = FastAPI()


def get_db() -> Session:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
def root():
    return {"message": "Hello World"}


@app.get("/books/", response_model=list[BookRead])
def read_books(
        db: Session = Depends(get_db),
        skip: int = 0,
        limit: int = 10,
        author_id: int | None = None
):
    return crud.get_all_books(db, author_id)


@app.post("/books/create", response_model=BookRead)
def create_book(
        book_data: BookCreate,
        db: Session = Depends(get_db)
):
    return crud.create_book(db, book_data)


@app.get("/authors/", response_model=list[AuthorRead])
def read_authors(
        db: Session = Depends(get_db),
        skip: int = 0,
        limit: int = 10,
):
    return crud.get_all_authors(db, skip, limit)


@app.post("/authors/create", response_model=AuthorRead)
def create_author(author_data: AuthorCreate,
                  db: Session = Depends(get_db)
                  ):
    author = crud.create_author(db, author_data)
    return author


@app.get("/authors/{author_id}", response_model=AuthorRead)
def author_by_id(author_id: int, db: Session = Depends(get_db)):
    author = get_author(db, author_id)
    return author
