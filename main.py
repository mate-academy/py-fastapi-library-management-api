from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Optional

import crud
import schemas
from database import SessionLocal

app = FastAPI()


def get_db() -> Session:
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()


@app.get("/authors/", response_model=list[schemas.Author])
def read_authors(
    db: Session = Depends(get_db), skip: int = 0, limit: int = 5
) -> list[schemas.Author]:
    return crud.get_all_authors(db, skip=skip, limit=limit)


@app.post("/authors/", response_model=schemas.Author)
def create_author(
    author: schemas.AuthorCreate,
    db: Session = Depends(get_db),
) -> schemas.Author:
    return crud.create_author(db, author)


@app.get("/authors/{author_id}/", response_model=schemas.Author)
def read_single_author(
    author_id: int, db: Session = Depends(get_db)
) -> schemas.Author:
    db_author = crud.get_author(db=db, author_id=author_id)

    if not db_author:
        raise HTTPException(status_code=404, detail="Author not found")

    return db_author


@app.get("/books/", response_model=list[schemas.Book])
def read_books(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 5,
    author_id: Optional[int] = None,
) -> list[schemas.Book]:
    return crud.get_all_books(db, skip=skip, limit=limit, author_id=author_id)


@app.post("/books/", response_model=schemas.BookCreate)
def create_book(
    book: schemas.BookCreate, db: Session = Depends(get_db)
) -> schemas.Book:
    return crud.create_book(db, book)
