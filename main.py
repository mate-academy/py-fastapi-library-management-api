from fastapi import FastAPI, Depends
from database import engine, get_db
from sqlalchemy.orm import Session
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
    db: Session = Depends(get_db)
):
    return crud.get_books(db, skip, limit)


@app.post("/books/")
def create_book(
    book: schemas.BookCreate,
    author_id: int,
    db: Session = Depends(get_db)
):
    return crud.create_book(db, book, author_id)


@app.get("/authors/{author_id}/books/")
def get_books_by_author(
    author_id: int,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    return crud.get_books_by_author(db, author_id, skip, limit)