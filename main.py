from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session

import models
import schemas
from database import SessionLocal, engine
import crud
app = FastAPI()
models.Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/authors/", response_model=schemas.AuthorResponse)
def create_author(author: schemas.AuthorCreate, db: Session = Depends(get_db)):
    author = crud.create_author(db=db, author=author)
    return author


@app.get("/authors/", response_model=list[schemas.AuthorResponse])
def read_authors(
        skip: int = 0,
        limit: int = 100,
        db: Session = Depends(get_db)
):
    authors = crud.get_authors(db=db, skip=skip, limit=limit)
    return authors


@app.post("/books/", response_model=schemas.BookResponse)
def create_book(book: schemas.BookCreate, db: Session = Depends(get_db)):
    book = crud.create_book(db=db, book=book)
    return book


@app.get(
    "/authors/{author_id}/books/",
    response_model=list[schemas.BookResponse]
)
def read_books_by_author(
        author_id: int,
        skip: int = 0,
        limit: int = 100,
        db: Session = Depends(get_db)
):
    books = crud.get_books_by_author(
        db=db,
        skip=skip,
        limit=limit,
        author_id=author_id
    )
    return books


@app.get("/authors/{author_id}/", response_model=schemas.AuthorResponse)
def get_author(author_id: int, db: Session = Depends(get_db)):
    author = crud.get_author(author_id=author_id, db=db)
    return author


@app.get("/books/", response_model=list[schemas.BookResponse])
def get_books(db: Session = Depends(get_db), skip: int = 0, limit: int = 100):
    books = crud.get_books(db=db, skip=skip, limit=limit)
    return books
