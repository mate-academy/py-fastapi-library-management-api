from typing import List, Optional

from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

import crud
import models
import schemas
from database import SessionLocal

app = FastAPI()

def get_db() -> Session:
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()

@app.get("/")
def root() -> dict:
    return {"message": "Welcome to the Library API"}

@app.get("/authors/", response_model=List[schemas.AuthorRead])
def read_all_authors(
        skip: int = 0,
        limit: int = 10,
        db: Session = Depends(get_db)
    ) -> List[models.Author]:
    return crud.get_all_authors(db=db, skip=skip, limit=limit)

@app.get("/authors/{author_id}", response_model=schemas.AuthorRead)
def read_author(author_id: int, db: Session = Depends(get_db)) -> models.Author:
    db_author = crud.get_author_by_id(db=db, author_id=author_id)

    if db_author is None:
        raise HTTPException(status_code=404, detail="Author not found")

    return db_author

@app.post("/authors/", response_model=schemas.AuthorRead)
def create_author(author: schemas.AuthorCreate, db: Session = Depends(get_db)) -> models.Author:
    existing = crud.get_author_by_name(db=db, name=author.name)

    if existing:
        raise HTTPException(status_code=400, detail="Author already exists")

    return crud.create_author(db=db, author=author)

@app.put("/authors/{author_id}", response_model=schemas.AuthorRead)
def update_author(author_id: int, author: schemas.AuthorCreate, db: Session = Depends(get_db)) -> models.Author:
    db_author = crud.get_author_by_id(db=db, author_id=author_id)

    if db_author is None:
        raise HTTPException(status_code=404, detail="Author not found")

    return crud.update_author(db=db, author_id=author_id, author=author)

@app.get("/books/", response_model=List[schemas.BookRead])
def read_all_books(
        skip: int = 0,
        limit: int = 10,
        author_id: Optional[int] = None,
        db: Session = Depends(get_db)
    ) -> List[models.Book]:
    if author_id:
        return crud.get_books_by_author_id(db=db, author_id=author_id, skip=skip, limit=limit)

    return crud.get_all_books(db=db, skip=skip, limit=limit)

@app.get("/books/{book_id}", response_model=schemas.BookRead)
def read_book(book_id: int, db: Session = Depends(get_db)) -> models.Book:
    db_book = crud.get_book_by_id(db=db, book_id=book_id)

    if db_book is None:
        raise HTTPException(status_code=404, detail="Book not found")

    return db_book


@app.put("/books/{book_id}", response_model=schemas.BookRead)
def update_book(book_id: int, book: schemas.BookCreate, db: Session = Depends(get_db)) -> models.Book:
    db_book = crud.get_book_by_id(db=db, book_id=book_id)

    if db_book is None:
        raise HTTPException(status_code=404, detail="Book not found")

    return crud.update_book(db=db, book_id=book_id, book=book)

@app.post("/books/", response_model=schemas.BookRead)
def create_book(book: schemas.BookCreate, db: Session = Depends(get_db)) -> models.Book:
    existing_book = crud.get_book_by_name(db=db, name=book.title)
    author = crud.get_author_by_id(db=db, author_id=book.author_id)

    if existing_book:
        raise HTTPException(status_code=400, detail="Book already exists")

    if not author:
        raise HTTPException(status_code=404, detail="Author not found")


    return crud.create_book(db=db, book=book)