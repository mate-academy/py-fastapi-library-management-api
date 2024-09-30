from fastapi import FastAPI, Depends, HTTPException
from typing import List
from sqlalchemy.orm import Session
import crud
from schemas import (
    Author,
    AuthorCreate,
    Book,
    BookCreate,
)
from database import SessionLocal

app = FastAPI()


def get_db() -> None:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/authors/", response_model=List[Author])
def get_authors(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)) -> List[Author]:
    return crud.get_authors(db=db, skip=skip, limit=limit)


@app.get("/authors/{author_id}", response_model=Author)
def get_author_by_id(author_id: int, db: Session = Depends(get_db)) -> Author:
    db_author = crud.get_author_by_id(db=db, author_id=author_id)
    if author_id is None:
        raise HTTPException(status_code=404, detail="Author not found")
    return db_author


@app.post("/authors/", response_model=Author)
def create_author(author: AuthorCreate, db: Session = Depends(get_db)) -> Author:
    return crud.create_author(db=db, author=author)


@app.get("/author/{author_id}/books", response_model=List[Book])
def get_books_by_author_id(author_id: int, skip: int = 0, limit: int = 10, db: Session = Depends(get_db)) -> List[Book]:
    return crud.get_books_by_author_id(db=db, author_id=author_id, skip=skip, limit=limit)


@app.get("/books/", response_model=List[Book])
def get_books(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)) -> List[Book]:
    return crud.get_books(db=db, skip=skip, limit=limit)


@app.post("/books/", response_model=Book)
def create_book(author_id: int, book: BookCreate, db: Session = Depends(get_db)) -> Book:
    return crud.create_book(db=db, book=book, author_id=author_id)

