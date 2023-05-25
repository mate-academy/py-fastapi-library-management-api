from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

import crud
import schemas
from db.engine import SessionLocal

app = FastAPI()


def get_db() -> Session:
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()


@app.get("/")
def root():
    return {"message": "Hello world!"}


@app.get("/authors/", response_model=list[schemas.Author])
def read_authors(
        skip: int = 0, limit: int = 10, db: Session = Depends(get_db)
):
    authors = crud.get_all_authors(db, skip=skip, limit=limit)
    return authors


@app.post("/authors/", response_model=schemas.Author)
def create_author(author: schemas.AuthorCreate, db: Session = Depends(get_db)):
    db_author = crud.create_author(db, author)
    return db_author


@app.get("/authors/{author_id}/", response_model=schemas.Author)
def read_author(author_id: int, db: Session = Depends(get_db)):
    author = crud.get_author_by_author_id(db, author_id)
    if author is None:
        raise HTTPException(status_code=404, detail="Author not found")
    return author


@app.get("/books/", response_model=list[schemas.Book])
def read_books(skip: int = 0, limit: int = 10,
               db: Session = Depends(get_db),
               author_id: int | None = None
               ):
    books = crud.get_all_books(db, skip=skip, limit=limit, author_id=author_id)
    return books


@app.get("/books/{book_id}", response_model=schemas.Book)
def read_book(book_id: int, db: Session = Depends(get_db)):
    book = crud.get_book_by_book_id(db, book_id)
    if book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    return book


@app.post("/books/", response_model=schemas.Book)
def create_book(
        book: schemas.BookCreate,
        db: Session = Depends(get_db),
):
    db_book = crud.create_book(db=db, book=book)
    return db_book
