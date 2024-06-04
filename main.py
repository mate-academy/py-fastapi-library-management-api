from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session

from database import SessionLocal

import crud
import schemas

app = FastAPI()


def get_db() -> Session:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/authors/", response_model=list[schemas.Author])
def read_authors(
    skip: int | None = 0,
    limit: int | None = 10,
    db: Session = Depends(get_db)
):
    return crud.get_all_authors(db, skip, limit)


@app.get("/authors/{author_id}/", response_model=schemas.Author)
def read_single_author(author_id: int, db: Session = Depends(get_db)):
    return crud.get_author(db, author_id)


@app.post("/authors/{author_id}/", response_model=schemas.Author)
def create_author(author: schemas.AuthorCreate, db: Session = Depends(get_db)):
    return crud.create_author(db, author)


@app.get("/books/", response_model=list[schemas.Book])
def read_books(
    author_id: int | None = None,
    skip: int | None = 0,
    limit: int | None = 10,
    db: Session = Depends(get_db)
):
    return crud.get_books(db, author_id, skip, limit)


@app.post("/books/", response_model=schemas.Book)
def create_book(book: schemas.BookCreate, db: Session = Depends(get_db)):
    return crud.create_book(db, book)
