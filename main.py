from typing import Any, Type

from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

import crud
from db import models
from db.engine import SessionLocal
from schemas import Authors, Books, CreateAuthor, CreateBook

app = FastAPI()


def get_db() -> Session:
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/authors/", response_model=list[Authors])
def read_authors(
        db: Session = Depends(get_db), skip: int = 0, limit: int = 100
) -> list[Type[models.Author]]:
    authors = crud.get_all_author(db, skip=skip, limit=limit)
    return authors


@app.post("/authors/", response_model=Authors)
def create_user(author: CreateAuthor, db: Session = Depends(get_db)) -> models.Author:
    return crud.create_author(db=db, author=author)


@app.get("/authors/{author_id}/", response_model=Authors)
def read_user(
        author_id: int, db: Session = Depends(get_db)
) -> list[Type[models.Author]] | None:
    db_author = crud.get_author(db, author_id=author_id)
    if db_author is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_author


@app.post("/authors/{author_id}/book/", response_model=Books)
def create_item_for_user(
    author_id: int, book: CreateBook, db: Session = Depends(get_db)
) -> models.Book:
    return crud.create_author_book(db=db, book=book, author_id=author_id)


@app.get("/books/", response_model=list[Books])
def read_books(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    author_id: str | None = None,
) -> list[Type[models.Book]] | []:
    books = crud.get_all_books(db, skip=skip, limit=limit, author_id=author_id)
    return books
