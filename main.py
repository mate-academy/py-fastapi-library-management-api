from typing import List

from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

import schema
import crud
from database import SessionLocal


def get_db() -> Session:
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()

app = FastAPI()


@app.get("/authors/", response_model=List[schema.Author])
def read_authors(
        limit: int = 10, skip: int = 0, db: Session = Depends(get_db)
) -> List[schema.Author]:
    return crud.get_all_authors(db, skip=skip, limit=limit)

@app.get("/author/{author_id}/", response_model=schema.Author)
def read_author(
        author_id: int, db: Session = Depends(get_db)
) -> schema.Author:
    db_author = crud.get_author_by_id(db, author_id)
    if db_author is None:
        raise HTTPException(status_code=404, detail="Author not found")
    return db_author

@app.post("/authors/", response_model=schema.Author)
def create_author(
        author: schema.AuthorCreate,
        db: Session = Depends(get_db)
) -> schema.Author:
    db_author = crud.get_author_by_id(db, author.id)
    if db_author:
        raise HTTPException(status_code=409, detail="Author already exists")
    return crud.create_new_author(db, author=author)

@app.get("/books/", response_model=List[schema.Book])
def read_books(
        skip: int = 0,
        limit: int = 100,
        db: Session = Depends(get_db)
) -> List[schema.Book]:
    return crud.get_all_books(db, skip=skip, limit=limit)

@app.post("/books/", response_model=schema.Book)
def create_book(
        book: schema.BookCreate,
        db: Session = Depends(get_db)
) -> schema.Book:
    return crud.create_new_book(db, book=book)
