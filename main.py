from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

import crud
import models
import schemas
from database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Library Management API"
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/authors/", response_model=schemas.AuthorCreate)
def create_author(author: schemas.AuthorCreate, db: Session = Depends(get_db)):
    return crud.create_author(db=db, author=author)


@app.get("/authors/", response_model=list[schemas.AuthorList])
def read_authors(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    db_authors = crud.get_authors(db=db, skip=skip, limit=limit)
    return db_authors


@app.get("/authors/{author_id}/", response_model=schemas.AuthorList)
def read_author(author_id: int, db: Session = Depends(get_db)):
    author = crud.get_author(db=db, author_id=author_id)
    if not author:
        raise HTTPException(
            status_code=400,
            detail="No such author!"
        )
    return author


@app.post("/books/", response_model=schemas.BookCreate)
def create_book(book: schemas.BookCreate, db: Session = Depends(get_db)):
    book = crud.create_book(db=db, book=book)
    return book


@app.get("/books/", response_model=schemas.BookList)
def read_books(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    db_books = crud.get_books(db=db, skip=skip, limit=limit)
    return db_books


@app.get("/books/{author_id}/", response_model=schemas.BookList)
def get_books_by_author_id(author_id: int, db: Session = Depends(get_db)):
    db_books = crud.get_books_by_author_id(db=db, author_id=author_id)
    return db_books
