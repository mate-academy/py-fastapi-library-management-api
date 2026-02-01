from typing import List

from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

import crud
import schemas
from database import SessionLocal

app = FastAPI()


def get_db() -> Session:
    db = SessionLocal

    try:
        yield db
    finally:
        db.close()


@app.post("/authors", response_model=schemas.AuthorResponse)
def create_author(author: schemas.AuthorCreate, db: Session = Depends(get_db)):
    return crud.create_author(db, author)


@app.get("/authors", response_model=List[schemas.AuthorResponse])
def get_authors(skip: int = 0, limit:int = 100, db: Session = Depends(get_db)):
    authors = crud.get_authors(db)
    return authors


@app.get("/authors/{author_id}", response_model=schemas.AuthorResponse)
def get_author(author_id: int, db: Session = Depends(get_db)):
    author = crud.get_author(db, author_id)
    if not author:
        raise HTTPException(status_code=404, detail="Author not found")
    return author


@app.delete("/authors/{author_id}", response_model=schemas.AuthorResponse)
def delete_author(author_id: int, db: Session = Depends(get_db)):
    author = crud.delete_author(db, author_id)
    if not author:
        raise HTTPException(status_code=404, detail="Author not found")
    return author


@app.post("/books", response_model=schemas.BookResponse)
def create_book(book: schemas.BookCreate, db: Session = Depends(get_db)):
    return crud.create_book(db, book)


@app.get("/books", response_model=List[schemas.BookResponse])
def get_books(skip: int = 0, limit: int = 10, author_id: int | None = None, db: Session = Depends(get_db)):
    books = crud.get_books(db)
    if author_id is not None:
        books = [b for b in books if b.author_id == author_id]
    return books[skip : skip + limit]


@app.get("/books/{book_id}", response_model=schemas.BookResponse)
def get_book(book_id: int, db: Session = Depends(get_db)):
    book = crud.get_book(db, book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return book


@app.delete("/books/{book_id}", response_model=schemas.BookResponse)
def delete_book(book_id: int, db: Session = Depends(get_db)):
    return crud.delete_book(db, book_id)
