from collections.abc import Generator

from fastapi import FastAPI, Depends, HTTPException, Query
from sqlalchemy.orm import Session

import crud
import models
import schemas
from database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()


# authors
@app.get("/authors/", response_model=list[schemas.AuthorRead])
def get_all_authors(
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=10, ge=1, le=100),
    db: Session = Depends(get_db),
):
    return crud.get_all_authors(db, skip=skip, limit=limit)


@app.get("/authors/{author_id}", response_model=schemas.AuthorRead)
def get_author(author_id: int, db: Session = Depends(get_db)):
    db_author = crud.get_author(db, author_id)

    if db_author is None:
        raise HTTPException(status_code=404, detail="Author not found")

    return db_author


@app.post("/authors/", response_model=schemas.AuthorRead)
def create_author(
    author: schemas.AuthorCreate,
    db: Session = Depends(get_db),
):
    if crud.get_author_by_name(db, author.name) is not None:
        raise HTTPException(status_code=400, detail="Author already exists")

    return crud.create_author(db=db, author=author)


# books
@app.get("/books/", response_model=list[schemas.BookRead])
def get_books(
    author_id: int | None = None,
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=10, ge=1, le=100),
    db: Session = Depends(get_db),
):
    return crud.get_books(db, author_id=author_id, skip=skip, limit=limit)


@app.post("/books/", response_model=schemas.BookRead)
def create_book(
    book: schemas.BookCreate,
    db: Session = Depends(get_db),
):
    if crud.get_author(db, book.author_id) is None:
        raise HTTPException(status_code=404, detail="Author not found")

    return crud.create_book(db=db, book=book)
