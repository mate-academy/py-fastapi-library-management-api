from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List

from database import engine, SessionLocal
from crud import create_author, get_author, get_authors, create_book, get_books
from models import Base
from schemas import Author, AuthorCreate, Book, BookCreate


Base.metadata.create_all(bind=engine)

app = FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/authors/", response_model=Author)
def create_author_endpoint(author: AuthorCreate, db: Session = Depends(get_db)):
    return create_author(db=db, author=author)


@app.get("/authors/", response_model=List[Author])
def get_authors_endpoint(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return get_authors(db=db, skip=skip, limit=limit)


@app.get("/authors/{author_id}", response_model=Author)
def get_author_endpoint(author_id: int, db: Session = Depends(get_db)):
    author = get_author(db=db, author_id=author_id)
    if author is None:
        raise HTTPException(status_code=404, detail="Author not found")
    return author


@app.post("/books/", response_model=Book)
def create_book_endpoint(book: BookCreate, db: Session = Depends(get_db)):
    return create_book(db=db, book=book)


@app.get("/books/", response_model=List[Book])
def get_books_endpoint(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return get_books(db=db, skip=skip, limit=limit)


@app.get("/authors/{author_id}/books", response_model=List[Book])
def get_books_by_author_endpoint(
    author_id: int, skip: int = 0, limit: int = 10, db: Session = Depends(get_db)
):
    author = get_author(db=db, author_id=author_id)
    if author is None:
        raise HTTPException(status_code=404, detail="Author not found")
    return author.books[skip : skip + limit]
