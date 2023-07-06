from fastapi import FastAPI, Depends, HTTPException
from fastapi import status
from sqlalchemy.orm import Session
from typing import List
from database import SessionLocal, engine
import models
import crud
import schemas

app = FastAPI()

models.Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post('/authors/', response_model=schemas.Author)
def create_author(author: schemas.AuthorCreate, db: Session = Depends(get_db)):
    db_author = crud.create_author(db, author)
    return db_author


@app.get('/authors/', response_model=List[schemas.Author])
def get_authors(
    skip: int = 0, limit: int = 100, db: Session = Depends(get_db)
):
    authors = crud.get_authors(db, skip=skip, limit=limit)
    return authors


@app.get('/authors/{author_id}', response_model=schemas.Author)
def get_author(author_id: int, db: Session = Depends(get_db)):
    author = crud.get_author(db, author_id)
    if not author:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail='Author not found'
        )
    return author


@app.post('/books/', response_model=schemas.Book)
def create_book(book: schemas.BookCreate, db: Session = Depends(get_db)):
    author = crud.get_author(db, book.author_id)
    if not author:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail='Author not found'
        )
    db_book = crud.create_book(db, book)
    return db_book


@app.get('/books/', response_model=List[schemas.Book])
def get_books(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    books = crud.get_books(db, skip=skip, limit=limit)
    return books


@app.get('/books/by_author/{author_id}', response_model=List[schemas.Book])
def get_books_by_author(
    author_id: int,
    skip: int = 0, limit: int = 100, db: Session = Depends(get_db)
):
    books = crud.get_books_by_author(db, author_id, skip=skip, limit=limit)
    return books
