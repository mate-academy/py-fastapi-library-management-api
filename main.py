from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

import schemas
import crud
from database import SessionLocal
from typing import List

app = FastAPI()
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def root() -> dict:
    return {"message": "FastAPI library"}

@app.get("/authors/", response_model=List[schemas.Author])
def get_authors(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)) -> list:
    return crud.get_authors(db=db, skip=skip, limit=limit)

@app.get("/authors/{author_id}", response_model=schemas.Author)
def get_author_by_id(author_id: int, db: Session = Depends(get_db)):
    return crud.get_author_by_id(db=db, author_id=author_id)

@app.post("/authors/", response_model=schemas.Author)
def create_author(
        author: schemas.AuthorCreate,
        db: Session = Depends(get_db)
):
    db_author = crud.get_author_by_name(db, author.name)
    if db_author:
        raise HTTPException(
            status_code=400,
            detail=f"Author {author.name} already exists"
        )
    return crud.create_author(db=db, author=author)

@app.get("/books/", response_model=List[schemas.Book])
def read_all_books(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    books = crud.get_books_list(db=db, skip=skip, limit=limit)
    return books


@app.get("/books/{author_id}", response_model=List[schemas.Book])
def get_book_by_author_id(author_id: int, db: Session = Depends(get_db)) -> list:
    db_books = crud.get_books_by_author_id(db=db, author_id=author_id)

    if db_books is None:
        raise HTTPException(status_code=404, detail=f"Books from {author_id} not found")

    return db_books


@app.post("/books/", response_model=schemas.Book)
def create_book(
        book: schemas.BookCreate,
        db: Session = Depends(get_db)
):
    db_book = crud.get_book_by_title(db, book.title)
    if db_book:
        raise HTTPException(
            status_code=400,
            detail=f"Book {book.title} is already exists"
        )

    return crud.create_book(db=db, book=book)



