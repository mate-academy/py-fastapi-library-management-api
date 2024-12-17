from fastapi import FastAPI, Depends, Query, HTTPException
from sqlalchemy.orm import Session

import crud
import schemas
from database import SessionLocal
from models import Book
from schemas import BookListResponse


app = FastAPI()


def get_db():
    db: Session = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/authors/", response_model=list[schemas.AuthorResponse])
def read_authors(
        skip: int = Query(0, ge=0),
        limit: int = Query(10, ge=1),
        db: Session = Depends(get_db)
):
    authors = crud.get_all_authors(db=db, skip=skip, limit=limit)
    return authors


@app.get("/authors/{author_id}", response_model=schemas.AuthorResponse)
def read_author_by_id(author_id: int, db: Session = Depends(get_db)):
    author = crud.get_author_by_id(db=db, author_id=author_id)
    if not author:
        raise HTTPException(status_code=404, detail="Author not found")
    return author


@app.post("/authors/", response_model=schemas.AuthorResponse)
def create_author(
        author: schemas.AuthorCreate,
        db: Session = Depends(get_db)
):
    return crud.create_author(db=db, author=author)


@app.get("/books/", response_model=BookListResponse)
def get_books(
        skip: int = Query(0, ge=0),
        limit: int = Query(10, ge=1),
        db: Session = Depends(get_db)
):
    books = crud.get_books(db=db, skip=skip, limit=limit)
    return {"books": books}


@app.post("/books/", response_model=schemas.BookResponse)
def create_book(
        book: schemas.BookCreate,
        db: Session = Depends(get_db)
):
    return crud.create_book(db=db, book=book)


@app.get("/books/{book_id}", response_model=schemas.BookResponse)
def create_book_by_id(
        book_id: int,
        db: Session = Depends(get_db)
):
    book = crud.get_book_by_id(db=db, book_id=book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return book
