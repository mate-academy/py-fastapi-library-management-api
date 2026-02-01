from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

from database import SessionLocal, engine, Base
from schemas import AuthorCreate, Author, BookCreate, Book
from crud import create_author, get_authors, get_author, create_book, get_books

from typing import List


Base.metadata.create_all(bind=engine)

app = FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/authors/", response_model=Author)
def create_new_author(author: AuthorCreate, db: Session = Depends(get_db)):
    return create_author(db, author)


@app.get("/authors/", response_model=List[Author])
def read_authors(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return get_authors(db, skip=skip, limit=limit)


@app.get("/authors/{author_id}", response_model=Author)
def read_author(author_id: int, db: Session = Depends(get_db)):
    author = get_author(db, author_id)
    if author is None:
        raise HTTPException(status_code=404, detail="Автор не знайдено")
    return author


@app.post("/authors/{author_id}/books/", response_model=Book)
def create_book_for_author(
        author_id: int,
        book: BookCreate,
        db: Session = Depends(get_db)
):
    author = get_author(db, author_id)
    if author is None:
        raise HTTPException(status_code=404, detail="Автор не знайдено")

    return create_book(db, book, author_id=author_id)


@app.get("/books/", response_model=List[Book])
def read_books(skip: int = 0, limit: int = 10, author_id: int = None, db: Session = Depends(get_db)):
    return get_books(db, skip=skip, limit=limit, author_id=author_id)
