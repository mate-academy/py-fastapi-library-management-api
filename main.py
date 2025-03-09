from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from database import engine, get_db

import models
import crud
import schemas

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


@app.post("/authors/", response_model=schemas.AuthorRead)
def create_author(author: schemas.AuthorCreate, db: Session = Depends(get_db)):
    return crud.create_author(db, author)


@app.get("/authors/", response_model=list[schemas.AuthorRead])
def get_authors(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return crud.get_authors(db, skip, limit)


@app.get("/authors/{author_id}", response_model=schemas.AuthorRead)
def get_author(author_id: int, db: Session = Depends(get_db)):
    author = crud.get_author(db, author_id)
    if author is None:
        raise HTTPException(status_code=404, detail="Author not found")
    return author


@app.post("/books/", response_model=schemas.BookRead)
def create_book(book: schemas.BookCreate, db: Session = Depends(get_db)):
    author = crud.get_author(db, book.author_id)
    if not author:
        raise HTTPException(status_code=404, detail="Author not found")
    return crud.create_book(db, book)


@app.get("/books/", response_model=list[schemas.BookRead])
def get_books(
        skip: int = 0,
        limit: int = 10,
        author_id: int | None = None,
        db: Session = Depends(get_db)
):
    return crud.get_books(db, skip, limit, author_id)
