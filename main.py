from typing import Annotated

from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

import crud
import models
from database import engine, SessionLocal
import schemas

models.Base.metadata.create_all(bind=engine)
app = FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


DBSession = Annotated[Session, Depends(get_db)]


@app.post("/authors/", response_model=schemas.Author, status_code=201)
def create_author(author: schemas.AuthorCreate, db: DBSession):
    if crud.get_author_by_name(db, author.name) is not None:
        raise HTTPException(status_code=400, detail="Author already exists")
    return crud.create_author(db, author)


@app.get("/authors/", response_model=list[schemas.Author], status_code=200)
def get_all_authors(db: DBSession, skip: int = 0, limit: int = 100):
    return crud.get_authors(db, skip, limit)


@app.get("/authors/{author_id}", response_model=schemas.Author, status_code=200)
def get_author(author_id: int, db: DBSession):
    db_author = crud.get_author(db, author_id)
    if db_author is None:
        raise HTTPException(status_code=404, detail="Author not found")
    return db_author


@app.post("/authors/{author_id}/books/", response_model=schemas.Book, status_code=201)
def create_book(book: schemas.BookCreate, author_id: int, db: DBSession):
    if crud.get_author(db, author_id) is None:
        raise HTTPException(status_code=404, detail="Author not found")
    return crud.create_book(db, book, author_id)


@app.get("/books/", response_model=list[schemas.Book], status_code=200)
def get_books(
    db: DBSession,
    skip: int = 0,
    limit: int = 100,
    author_id: int | None = None,
):
    return crud.get_books(db, skip, limit, author_id)
