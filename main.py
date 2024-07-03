from typing import List

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

from db.crud import get_authors, get_author, get_books, get_books_by_author
from db.database import SessionLocal, engine, Base
from db.schemas import Book, AuthorCreate, Author, BookCreate

Base.metadata.create_all(bind=engine)

app = FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/authors/", response_model=Author)
def create_author(author: AuthorCreate, db: Session = Depends(get_db)):
    return create_author(db=db, author=author)


@app.get("/authors/", response_model=List[Author])
def read_authors(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    authors = get_authors(db, skip=skip, limit=limit)
    return authors


@app.get("/authors/{author_id}", response_model=Author)
def read_author(author_id: int, db: Session = Depends(get_db)):
    db_author = get_author(db, author_id=author_id)
    if db_author is None:
        raise HTTPException(status_code=404, detail="Author not found")
    return db_author


@app.post("/books/", response_model=Book)
def create_book(book: BookCreate, db: Session = Depends(get_db)):
    return create_book(db=db, book=book)


@app.get("/books/", response_model=List[Book])
def read_books(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    books = get_books(db, skip=skip, limit=limit)
    return books


@app.get("/books/author/{author_id}", response_model=List[Book])
def read_books_by_author(author_id: int, skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    books = get_books_by_author(db, author_id=author_id, skip=skip, limit=limit)
    return books
