from typing import List

from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
import crud
import schemas
import models
import database

models.Base.metadata.create_all(bind=database.engine)

app = FastAPI()


@app.get("/")
def read_root():
    return {"message": "Welcome to Libraty Management API!"}


def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/authors/", response_model=schemas.AuthorRead)
def create_author(author: schemas.AuthorCreate,
                  db: Session = Depends(get_db)):
    return crud.create_author(db=db, author=author)


@app.get("/authors/", response_model=List[schemas.AuthorRead])
def get_authors(
        skip: int = 0,
        limit: int = 100,
        db: Session = Depends(get_db)
):
    authors = crud.get_authors(db=db, skip=skip, limit=limit)
    return authors


@app.get("/authors/{author_id}/", response_model=List[schemas.AuthorRead])
def get_author(author_id: int,
               db: Session = Depends(get_db)):
    db_author = crud.get_authors(db=db, author_id=author_id)
    if db_author is None:
        raise HTTPException(status_code=404, detail="Author not found")
    return db_author


@app.post("/books/", response_model=schemas.Book)
def create_book(
        book: schemas.BookCreate,
        db: Session = Depends(get_db)):
    if not book.author_id:
        raise HTTPException(status_code=404, detail="Author not found")

    try:
        return crud.create_book(db=db, book=book, author_id=book.author_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/books/", response_model=List[schemas.Book])
def get_books(
        skip: int = 0,
        limit: int = 100,
        db: Session = Depends(get_db)):
    books = crud.get_books(db=db, skip=skip, limit=limit)
    return books


@app.get("/books/author/{author_id}", response_model=List[schemas.Book])
def get_book_by_author(
        author_id: int,
        db: Session = Depends(get_db)
):
    books = crud.get_book_by_author(
        db=db,
        author_id=author_id)
    return books
