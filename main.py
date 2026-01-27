from typing import Generator

from fastapi import FastAPI, Depends, Query
from sqlalchemy.orm import Session

import crud
import models
import schemas
from database import SessionLocal

app = FastAPI()
models.Base.metadata.create_all(bind=engine)

def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()


@app.get("/")
def root() -> dict:
    return {"message": "Hello"}


@app.get("/authors/", response_model=list[schemas.Author])
def list_authors(
    db: Session = Depends(get_db),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
) -> list[schemas.Author]:
    return crud.get_authors(db, skip=skip, limit=limit)


@app.get("/authors/{author_id}/", response_model=schemas.Author)
def get_author(author_id: int, db: Session = Depends(get_db)) -> schemas.Author:
    return crud.get_author_by_id(db, author_id=author_id)


@app.post("/authors/", response_model=schemas.Author)
def create_author(
    author_data: schemas.AuthorCreate, db: Session = Depends(get_db)
) -> schemas.Author:
    return crud.create_author(db, author_data=author_data)


@app.get("/books/", response_model=list[schemas.Book])
def list_books(
    db: Session = Depends(get_db),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    author_id: int = Query(None, ge=1),
) -> list[schemas.Book]:
    return crud.get_books(db, author_id=author_id, skip=skip, limit=limit)


@app.post("/books/", response_model=schemas.Book)
def create_book(
    book_data: schemas.BookCreate, db: Session = Depends(get_db)
) -> schemas.Book:
    return crud.create_book(db, book_data=book_data)
