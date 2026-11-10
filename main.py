from fastapi import FastAPI, Depends
from database import engine, get_db
from sqlalchemy.orm import Session
from typing import Optional
import models
import crud
import schemas


models.Base.metadata.create_all(bind = engine)
app = FastAPI()
@app.post("/authors/")
def create_author(
    author: schemas.AuthorCreate,
    db: Session = Depends(get_db)
):
    return crud.create_author(db, author)


@app.get("/authors/{author_id}")
def get_author(author_id: int, db: Session = Depends(get_db)):
    return crud.get_author(db, author_id)



@app.get("/authors/")
def get_authors(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    return crud.get_authors(db, skip, limit)


@app.get("/books/")
def get_books(
    skip: int = 0,
    limit: int = 100,
    author_id: Optional[int] = None,
    db: Session = Depends(get_db)
):
    if author_id is not None:
        return crud.get_books_by_author(db, author_id, skip, limit)
    else:
        return crud.get_books(db, skip, limit)


@app.post("/books/")
def create_book(
    book: schemas.BookCreate,
    db: Session = Depends(get_db)
):
    return crud.create_book(db, book)


@app.get("/authors/{author_id}/books/")
def get_books_by_author(
    author_id: int,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    return crud.get_books_by_author(db, author_id, skip, limit)