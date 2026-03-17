from typing import Generator

from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Any

import models
import schemas
import crud
from database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


def get_db() -> Generator[Session, Any, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/authors/", response_model=schemas.Author)
def create_author(
    author: schemas.AuthorCreate,
    db: Session = Depends(get_db)
) -> models.Author:
    existing_author = crud.get_author_by_name(db, author.name)
    if existing_author:
        raise HTTPException(
            status_code=409,
            detail="Author already exists"
        )

    return crud.create_author(db, author)


@app.get("/authors/", response_model=list[schemas.Author])
def read_authors(
    skip: int = 0, limit: int = 10, db: Session = Depends(get_db)
) -> schemas.List[models.Author]:
    return crud.get_authors(db, skip=skip, limit=limit)


@app.get("/authors/{author_id}", response_model=schemas.Author)
def read_author(
    author_id: int,
    db: Session = Depends(get_db)
) -> models.Author:
    db_author = crud.get_author(db, author_id)
    if not db_author:
        raise HTTPException(status_code=404, detail="Author not found")
    return db_author


@app.post("/authors/{author_id}/books/", response_model=schemas.Book)
def create_book_for_author(
    author_id: int,
    book: schemas.BookCreate,
    db: Session = Depends(get_db)
) -> models.Book:
    author = crud.get_author(db, author_id)
    if not author:
        raise HTTPException(
            status_code=404,
            detail="Author not found"
        )

    return crud.create_book(db, book, author_id)


@app.get("/books/", response_model=list[schemas.Book])
def read_books(
    skip: int = 0, limit: int = 10, db: Session = Depends(get_db)
) -> schemas.List[models.Book]:
    return crud.get_books(db, skip=skip, limit=limit)


@app.get("/authors/{author_id}/books/", response_model=list[schemas.Book])
def read_books_by_author(
    author_id: int, skip: int = 0,
    limit: int = 10,
    db: Session = Depends(get_db)
) -> schemas.List[models.Book]:
    return crud.get_books_by_author(db, author_id, skip, limit)
