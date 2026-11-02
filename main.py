from collections.abc import Iterator

from fastapi import FastAPI
from fastapi.params import Depends
from sqlalchemy.orm import Session

import crud
import schemas
from database import Base, SessionLocal, engine

Base.metadata.create_all(bind=engine)

app = FastAPI()


def get_db() -> Iterator[Session]:
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()


@app.get("/authors/", response_model=list[schemas.AuthorRead])
def read_authors(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
):
    return crud.get_all_authors(db=db, skip=skip, limit=limit)


@app.get("/authors/{author_id}", response_model=schemas.AuthorRead | None)
def read_author(author_id: int, db: Session = Depends(get_db)):
    return crud.get_author(db, author_id)


@app.post("/authors/", response_model=schemas.AuthorRead)
def create_author(author: schemas.AuthorCreate, db: Session = Depends(get_db)):
    return crud.create_author(author=author, db=db)


@app.post(
    "/authors/{author_id}/books/",
    response_model=schemas.BookRead,
)
def create_book(
    author_id: int, book: schemas.BookCreate, db: Session = Depends(get_db)
):
    return crud.create_book(db=db, book=book, author_id=author_id)


@app.get("/books/", response_model=list[schemas.BookRead])
def read_books(
    skip: int = 0,
    limit: int = 100,
    author_id: int | None = None,
    db: Session = Depends(get_db),
):
    return crud.get_all_books(db=db, skip=skip, limit=limit, author_id=author_id)
