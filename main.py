from http.client import HTTPException
from typing import List

from fastapi import FastAPI
from fastapi.params import Depends
from sqlalchemy.orm import Session

import crud
import database
import models
import schemas
from database import SessionLocal

models.Base.metadata.create_all(bind=database.engine)

app = FastAPI()


def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()


@app.get("/")
def root():
    return {"message": "Hello, World"}


@app.get("/authors/", response_model=list[schemas.Author])
def read_authors(db: Session = Depends(get_db)):
    return crud.get_all_author_list(db=db)


@app.post("/authors/", response_model=schemas.Author)
def create_authors(author: schemas.AuthorCreate, db: Session = Depends(get_db)):
    return crud.create_author(db=db, author=author)


@app.get("/authors/{author_id}", response_model=schemas.Author)
def get_author(author_id: int, db: Session = Depends(get_db)):
    db_author = crud.get_author(db=db, author_id=author_id)
    if db_author is None:
        raise HTTPException(status_code=404, detail="Author is not found")
    return db_author


@app.get("/books/", response_model=list[schemas.Book])
def read_books(
    db: Session = Depends(get_db),
):
    return crud.get_book_list(db=db)


@app.get("/books/author/{author_id}", response_model=List[schemas.Book])
def get_books_by_author(author_id: int, db: Session = Depends(get_db)):
    books = crud.get_books_by_author(db=db, author_id=author_id)
    return books


@app.post("/books/", response_model=schemas.Book)
def create_book(
    book: schemas.BookCreate,
    author_id: int,
    db: Session = Depends(get_db),
):
    return crud.create_book(db=db, book=book, author_id=author_id)
