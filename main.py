from typing import List

from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

import crud
from db.engine import SessionLocal
from schemas import Author, AuthorCreate, Book, BookCreate

app = FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/authors/", response_model=Author)
def create_author(author: AuthorCreate, db: Session = Depends(get_db)):
    db_author = crud.get_author_by_name(db, name=author.name)
    if db_author:
        raise HTTPException(status_code=400, detail="Author already registered")
    return crud.create_author(db=db, author=author)


@app.get("/authors/", response_model=List[Author])
def read_authors(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    authors = crud.get_authors_with_pagination(db, skip=skip, limit=limit)
    return authors


@app.get("/authors/{author_id}", response_model=Author)
def read_author(author_id: int, db: Session = Depends(get_db)):
    db_author = crud.get_author_by_id(db, author_id=author_id)
    if db_author is None:
        raise HTTPException(status_code=404, detail="Author not found")
    return db_author


@app.post("/books/", response_model=Book)
async def create_book(book: BookCreate, db: Session = Depends(get_db)):
    created_book = crud.create_book(db=db, book=book)
    return created_book


@app.get("/books/", response_model=List[Book])
def read_books(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    books = crud.get_books_with_pagination(db, skip=skip, limit=limit)
    return books


@app.get("/authors/{author_id}/books", response_model=List[Book])
def read_books_by_author(author_id: int, db: Session = Depends(get_db)):
    books = crud.get_books_by_author(db, author_id=author_id)
    return books
