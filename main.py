from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from collections.abc import Generator

import schemas
import crud
from db.engine import SessionLocal, Base, engine
from db import models


Base.metadata.create_all(bind=engine)

app = FastAPI()


def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
def root():
    return {"message": "Library Management API is running!"}


@app.post("/authors/", response_model=schemas.Author)
def create_author(author: schemas.AuthorCreate, db: Session = Depends(get_db)):
    existing_author = db.query(models.Author).filter(models.Author.name == author.name).first()
    if existing_author:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Author with name '{author.name}' already exists."
        )
    return crud.create_author(db, author)


@app.get("/authors/", response_model=list[schemas.Author])
def read_authors(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_authors(db, skip=skip, limit=limit)


@app.get("/authors/{author_id}", response_model=schemas.Author)
def read_author(author_id: int, db: Session = Depends(get_db)):
    author = crud.get_author(db, author_id)
    if not author:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Author with id '{author.id}' not found."
        )
    return crud.get_author(db, author_id)


@app.post("/books/", response_model=schemas.Book)
def create_book(book: schemas.BookCreate, db: Session = Depends(get_db)):
    author = crud.get_author(db, book.author_id)
    if not author:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Author with id '{book.author_id}' not found."
        )
    return crud.create_book(db, book)


@app.get("/books/", response_model=list[schemas.Book])
def read_books(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_books(db, skip=skip, limit=limit)


@app.get("/books/by_author/{author_id}", response_model=list[schemas.Book])
def read_books_by_author(author_id: int, db: Session = Depends(get_db)):
    author = crud.get_author(db, author_id)
    if not author:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Author with id '{author_id}' not found."
        )
    return crud.get_books_by_author(db, author_id)
