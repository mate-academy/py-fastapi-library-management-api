from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

from crud import (
    create_author,
    get_all_authors,
    get_author,
    create_book,
    get_all_books
)
from database import SessionLocal
from schemas import Author, AuthorCreate, Book, BookCreate

app = FastAPI()


def get_db() -> Session:
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()

@app.get("/")
def read_root() -> dict:
    return {"Library": "Service"}


@app.post("/authors/", response_model=Author)
def create_new_author(
        author: AuthorCreate,
        db: Session = Depends(get_db)
):
    db_author = create_author(db, author)
    return db_author


@app.get("/authors/", response_model=list[Author])
def get_author_list(
        skip: int = 0,
        limit: int = 100,
        db: Session = Depends(get_db)
):
    authors = get_all_authors(db, skip=skip, limit=limit)
    return authors

@app.get("/authors/{author_id}/", response_model=Author)
def get_author_by_id(
        author_id: int,
        db: Session = Depends(get_db)
):
    author = get_author(db, author_id)
    if not author:
        raise HTTPException(status_code=404, detail="Author not found")
    return author


@app.post("/books/", response_model=Book)
def create_new_book(
        author_id: int,
        book: BookCreate,
        db: Session = Depends(get_db)
):
    author = get_author(db, author_id)
    if not author:
        raise HTTPException(status_code=404, detail="Author not found")
    book.author_id = author_id
    db_book = create_book(db, book)
    return db_book


@app.get("/books/", response_model=list[Book])
def get_books_list(
        skip: int = 0,
        limit: int = 100,
        db: Session = Depends(get_db)
):
    books = get_all_books(db, skip=skip, limit=limit)
    return books

@app.get("/books/author/{author_id}/", response_model=list[Book])
def get_book_by_author_id(
        author_id: int,
        db: Session = Depends(get_db)
):
    books  = db.query(Book).filter(Book.author_id == author_id).all()
    return books
