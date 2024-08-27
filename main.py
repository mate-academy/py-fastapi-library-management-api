from typing import List
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

import crud
import schemas
from db import models
from db.database import SessionLocal

app = FastAPI()


def get_db() -> Session:
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()


@app.get("/authors/", response_model=List[schemas.Author])
def read_authors(
        limit: int = 10,
        skip: int = 0,
        db: Session = Depends(get_db)
) -> List[models.Author]:
    return crud.all_authors(db, skip=skip, limit=limit)


@app.get("/authors/{author_id}/", response_model=schemas.Author)
def read_single_authors(
        author_id: int,
        db: Session = Depends(get_db)
) -> models.Author:
    db_author = crud.get_single_author_by_id(db, author_id)

    if db_author is None:
        raise HTTPException(status_code=404, detail="Author not found")

    return db_author


@app.post("/authors/", response_model=schemas.Author)
def create_author(
        author: schemas.AuthorCreate,
        db: Session = Depends(get_db)
) -> models.Author:
    db_author = crud.get_author_by_name(db, author.name)

    if db_author:
        raise HTTPException(status_code=400, detail="Author already exists")

    return crud.create_author(db, author=author)


@app.get("/books/", response_model=List[schemas.Book])
def read_books(
        author_id: int = None,
        skip: int = 0,
        limit: int = 10,
        db: Session = Depends(get_db)
) -> List[models.Book]:
    return crud.all_books(db, skip=skip, limit=limit, author_id=author_id)


@app.post("/books/", response_model=schemas.Book)
def read_books(
        book: schemas.BookCreate,
        db: Session = Depends(get_db)
) -> models.Book:
    return crud.create_book(db, book=book)
