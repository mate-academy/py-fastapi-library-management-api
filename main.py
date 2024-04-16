from typing import List

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

import crud
import models
import schemas
from database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/authors/", response_model=schemas.Author)
def create_author(author: schemas.AuthorCreate, db: Session = Depends(get_db)):
    return crud.create_author(db=db, author=author)


@app.get("/authors/", response_model=List[schemas.Author])
def read_authors(db: Session = Depends(get_db)):
    authors = crud.get_all_authors(db=db)
    return authors


@app.get("/authors/{author_id}/", response_model=schemas.Author)
def read_author(author_id: int, db: Session = Depends(get_db)):
    author = crud.get_author_by_id(db=db, author_id=author_id)
    if author is None:
        raise HTTPException(status_code=404, detail="Author not found")
    return author


@app.get("/authors/{author_id}/books/", response_model=List[schemas.Book])
def read_books_by_author(author_id: int, db: Session = Depends(get_db)):
    books = crud.get_books_by_author(db=db, author_id=author_id)
    return books


@app.post("/authors/{author_id}/books/", response_model=schemas.Book)
def create_book_for_author(book: schemas.BookCreate, db: Session = Depends(get_db)):
    return crud.create_book(db=db, book=book)


@app.get("/books/", response_model=List[schemas.Book])
def read_books_by_author(author_id: int, db: Session = Depends(get_db)):
    books = crud.get_books_by_author(db=db, author_id=author_id)
    return books
