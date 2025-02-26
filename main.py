from fastapi import FastAPI
from fastapi.params import Depends
from sqlalchemy.orm import Session

import crud
from database import SessionLocal
from schemas import (Author, Book,
                     AuthorCreate, BookCreate)

app = FastAPI()

def get_db():
    db = SessionLocal

    try:
        yield db
    finally:
        db.close()

@app.get("/")
def read_root():
    return {"message": "FastAPI works!"}

@app.get("/authors/", response_model=list[Author])
def read_authors(db: Session = Depends(get_db)):
    return crud.get_all_authors(db)

@app.get("/authors/{author_id}", response_model=Author)
def read_author(author_id: int, db: Session = Depends(get_db)):
    return crud.get_author_by_id(db, author_id)

@app.post("/authors/", response_model=Author)
def create_author(
    author: AuthorCreate,
    db: Session = Depends(get_db)
):
    return crud.create_author(db=db, author=author)

@app.get("/books/", response_model=list[Book])
def read_books(db: Session = Depends(get_db)):
    return crud.get_all_books(db)

@app.get("/books/author/{author_id}", response_model=list[Book])
def read_books_by_author(author_id: int, db: Session = Depends(get_db)):
    return crud.get_books_by_author_id(db, author_id)

@app.post("/books/", response_model=Book)
def create_book(
    book: BookCreate,
    db: Session = Depends(get_db)
):
    return crud.create_book(db=db, book=book)
