from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from db import models
import crud
from db.engine import SessionLocal
from schemas import AuthorCreate, BookCreate, Author, AuthorPaginated, Book, BookPaginated

app = FastAPI


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
def root():
    return {"message": "Hello World"}


@app.get("/authors/", response_model=AuthorPaginated)
def get_authors(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    authors = crud.get_all_authors(db, skip, limit)
    total = db.query(models.DBAuthor).count()
    pagination = {
        "total": total,
        "skip": skip,
        "limit": limit
    }
    return AuthorPaginated(pagination=pagination, items=authors)


@app.get("/authors/{author_id}", response_model=Author)
def get_author(author_id: int, db: Session = Depends(get_db)):
    author = crud.get_author_by_id(db, author_id)
    return author


@app.post("/authors/", response_model=Author)
def create_author(author: AuthorCreate, db: Session = Depends(get_db)):
    new_author = crud.create_author(db, author)
    return new_author


@app.post("/authors/{author_id}/books/", response_model=Book)
def create_book(author_id: int, book: BookCreate, db: Session = Depends(get_db)):
    new_book = crud.create_book_for_author(db, author_id, book)
    return new_book


@app.get("/books/", response_model=BookPaginated)
def get_books(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    books = crud.get_books(db, skip, limit)
    return books


@app.get("/books/filter/", response_model=BookPaginated)
def filter_books(author_id: int, skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    books = crud.filter_books_by_author_id(db, author_id, skip, limit)
    return books
