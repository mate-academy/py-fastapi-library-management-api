# main.py
from typing import List

from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

import crud
import schemas
from db.database import SessionLocal

app = FastAPI()


def get_db() -> Session:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/authors/", response_model=List[schemas.Author])
def read_authors(db: Session = Depends(get_db)):
    return crud.get_all_author(db=db)


@app.post("/authors/", response_model=schemas.Author)
def create_author(
    author : schemas.AuthorCreate,
    db: Session = Depends(get_db),
):
    db_author = crud.get_author_by_name(db=db, name=author.name)

    if db_author:
        raise HTTPException(status_code=400, detail="Author already exists")

    return crud.create_author(db=db, author=author)

@app.get("/books/", response_model=List[schemas.Book])
def read_books(db: Session = Depends(get_db)):
    return crud.get_all_book(db=db)


@app.post("/books/", response_model=schemas.Book)
def create_book(
        book : schemas.BookCreate,
        db: Session = Depends(get_db),
):
    return crud.create_book(db=db, book=book)


@app.get("/books/{id}", response_model=schemas.Book)
def read_book(
        book_id: int,
        db: Session = Depends(get_db)):

    db_book = crud.get_book_by_id(db=db, book_id=book_id)

    if not db_book:
        raise HTTPException(status_code=404, detail="Book not found")
    return db_book

