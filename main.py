from typing import List

from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from database import SessionLocal, engine
from crud import (
    create_author,
    get_author,
    get_authors,
    create_book,
    get_books,
)
from models import Base
from schemas import AuthorCreate, BookCreate, Author, Book

app = FastAPI()

Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.post("/authors/", response_model=Author)
def create_new_author(author: AuthorCreate, db: Session = Depends(get_db)):
    return create_author(db, author)


@app.get("/authors/", response_model=List[Author])
def retrieve_authors(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return get_authors(db, skip, limit)


@app.get("/authors/{author_id}", response_model=Author)
def retrieve_author(author_id: int, db: Session = Depends(get_db)):
    author = get_author(db, author_id)
    if not author:
        raise HTTPException(status_code=404, detail="Author not found")
    return author


@app.get("/books/", response_model=List[Book])
def retrieve_books(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return get_books(db, skip, limit)


@app.get("/books/by_author/", response_model=List[Book])
def filter_books_by_author(author_id: int, db: Session = Depends(get_db)):
    return db.query(Book).filter(Book.author_id == author_id).all()


@app.post("/books/", response_model=BookCreate)
def create_book(book: BookCreate, db: Session = Depends(get_db)):
    return create_book(db=db, book=book)
