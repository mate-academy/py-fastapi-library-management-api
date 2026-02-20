from typing import Generator

from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

import crud
import schemas
from database import SessionLocal, Base, engine


Base.metadata.create_all(bind=engine)

app = FastAPI()


def get_db() -> Generator:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
def root():
    return {"Hello": "World"}


@app.get("/authors/", response_model=list[schemas.Author])
def get_authors(db: Session = Depends(get_db), skip: int = 0, limit: int = 100):
    return crud.get_all_authors(db, skip, limit)


@app.get("/authors/{author_id}", response_model=schemas.Author)
def get_author_by_id(author_id: int, db: Session = Depends(get_db)):
    author = crud.get_author(db, author_id)
    if not author:
        raise HTTPException(status_code=404, detail="Author not found")

    return author


@app.post("/authors/", response_model=schemas.Author)
def create_author(author: schemas.AuthorCreate, db: Session = Depends(get_db)):

    if crud.get_author_by_name(db, author.name):
        raise HTTPException(status_code=400, detail="Author already exists")

    return crud.create_author(db, author)


@app.get("/books/", response_model=list[schemas.Book])
def get_books(db: Session = Depends(get_db), skip: int = 0, limit: int = 100):
    return crud.get_all_books(db, skip, limit)


@app.get("/books/{author_id}", response_model=list[schemas.Book])
def get_books_by_id(author_id: int, db: Session = Depends(get_db), skip: int = 0, limit: int = 100):

    if not crud.get_author(db, author_id):
        raise HTTPException(status_code=404, detail="Author not found")

    return crud.get_books_by_author_id(db, author_id, skip, limit)


@app.post("/books/", response_model=schemas.Book)
def create_book(book: schemas.BookCreate, db: Session = Depends(get_db)):
    author = crud.get_author(db, author_id=book.author_id)

    if not author:
        raise HTTPException(status_code=404, detail="Author not found")

    created_book = crud.create_book(db, book)
    return created_book
