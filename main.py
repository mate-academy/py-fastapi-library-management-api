from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

import crud
import models
import schemas
from database import SessionLocal, engine

app = FastAPI()
models.Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/authors/", response_model=list[schemas.AuthorRead])
def get_authors(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    authors = crud.get_all_authors(db=db, skip=skip, limit=limit)
    return authors


@app.get("/authors/{author_id}", response_model=schemas.AuthorRead)
def get_author(author_id: int, db: Session = Depends(get_db)):
    author = crud.get_author_by_id(db, author_id)
    if not author:
        raise HTTPException(status_code=404, detail="Author not found")
    return author


@app.post("/authors/", response_model=schemas.AuthorRead)
def create_author(
    author: schemas.AuthorCreate,
    db: Session = Depends(get_db),
):
    existing = crud.get_author_by_name(db, author.name)
    if existing:
        raise HTTPException(status_code=400, detail="Author already exists")

    return crud.create_author(db, author)


@app.get("/books/", response_model=list[schemas.BookRead])
def get_books(
    skip: int = 0,
    limit: int = 100,
    author_id: int | None = None,
    db: Session = Depends(get_db),
):
    books = crud.get_all_books(db=db, skip=skip, limit=limit, author_id=author_id)
    return books


@app.get("/books/{book_id}", response_model=schemas.BookRead)
def get_book(book_id: int, db: Session = Depends(get_db)):
    book = crud.get_book_by_id(db, book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return book


@app.post("/books/", response_model=schemas.BookRead)
def create_book(book: schemas.BookCreate, db: Session = Depends(get_db)):
    return crud.create_book(db, book)
