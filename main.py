from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional

import models
import schemas
import crud
from database import engine, Base, get_db

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Library Management API")


@app.post("/authors/", response_model=schemas.AuthorRead)
def create_author(author: schemas.AuthorCreate, db: Session = Depends(get_db)):
    db_author = crud.create_author(db, author)
    return db_author

@app.get("/authors/", response_model=List[schemas.AuthorRead])
def list_authors(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    authors = crud.get_authors(db, skip=skip, limit=limit)
    return authors

@app.get("/authors/{author_id}", response_model=schemas.AuthorRead)
def get_author(author_id: int, db: Session = Depends(get_db)):
    author = crud.get_author(db, author_id)
    if not author:
        raise HTTPException(status_code=404, detail="Author not found")
    return author


@app.post("/books/", response_model=schemas.BookRead)
def create_book(book: schemas.BookCreate, db: Session = Depends(get_db)):
    # Перевіримо, чи існує автор
    author = crud.get_author(db, book.author_id)
    if not author:
        raise HTTPException(status_code=404, detail="Author not found")
    db_book = crud.create_book(db, book)
    return db_book

@app.get("/books/", response_model=List[schemas.BookRead])
def list_books(skip: int = 0, limit: int = 100, author_id: Optional[int] = None, db: Session = Depends(get_db)):
    books = crud.get_books(db, skip=skip, limit=limit, author_id=author_id)
    return books
