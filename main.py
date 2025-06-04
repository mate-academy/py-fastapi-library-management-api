from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

import crud
import models
import schemas
from database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/authors/", response_model=schemas.Author)
def create_author(author: schemas.AuthorCreate, db: Session = Depends(get_db)):
    return crud.create_author(db, author)


@app.get("/authors/", response_model=list[schemas.Author])
def get_authors(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    authors = db.query(models.DBAuthor).offset(skip).limit(limit).all()
    return authors


@app.get("/authors/{author_id}", response_model=schemas.Author)
def get_author(author_id: int, db: Session = Depends(get_db)):
    author = crud.get_author_by_id(db, author_id)
    if not author:
        raise HTTPException(status_code=404, detail="Author not found")
    return author


@app.post("/books/", response_model=schemas.Book)
def create_book(book: schemas.BookCreate, db: Session = Depends(get_db)):
    return crud.create_book(db, book)


@app.get("/books/", response_model=list[schemas.Book])
def get_books(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    books = db.query(models.DBBook).offset(skip).limit(limit).all()
    return books


@app.get("/books/{book_id}", response_model=schemas.Book)
def get_book(book_id: int, db: Session = Depends(get_db)):
    book = crud.get_book_by_id(db, book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return book


@app.get("/books/by_author/{author_id}", response_model=list[schemas.Book])
def get_books_by_author(author_id: int, db: Session = Depends(get_db)):
    books = db.query(models.DBBook).filter(
        models.DBBook.author_id == author_id
    ).all()
    return books
