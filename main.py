from typing import Union

from fastapi import FastAPI, Depends, Query
from sqlalchemy.orm import Session

import crud
import schemas
from database import Base, engine, get_db

app = FastAPI()

Base.metadata.create_all(bind=engine)


@app.post("/authors/create/", response_model=schemas.Author)
def create_author(author: schemas.AuthorCreate, db: Session = Depends(get_db)):
    return crud.create_author(db, author)


@app.post("/books/create/", response_model=schemas.Book)
def create_book(book: schemas.BookCreate, db: Session = Depends(get_db)):
    return crud.create_book(db, book)


@app.get("/authors/", response_model=list[schemas.Author])
def get_authors(
    db: Session = Depends(get_db),
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100)
):
    return crud.get_authors(db, skip, limit)


@app.get("/authors/{item_id}", response_model=schemas.Author)
def get_author(author_id: int, db: Session = Depends(get_db)):
    return crud.get_author(db, author_id)


@app.get("/books/", response_model=list[schemas.Book])
def get_books(
    db: Session = Depends(get_db),
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100)
):
    return crud.get_books(db, skip, limit)


@app.get("/books/{item_id}", response_model=schemas.Book)
def get_book(book_id: int, db: Session = Depends(get_db)):
    return crud.get_book(db, book_id)
