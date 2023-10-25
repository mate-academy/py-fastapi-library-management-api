from fastapi import FastAPI, Depends, HTTPException, Query
from sqlalchemy.orm import Session

import crud
import schemas
from database import SessionLocal

app = FastAPI()


def get_db() -> Session:
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()


@app.get("/authors/", response_model=list[schemas.Author])
def get_authors(
        skip: int = Query(0, alias="skip"),
        limit: int = Query(10, alias="limit"),
        db: Session = Depends(get_db)
):
    authors = crud.get_all_authors(db)
    return authors[skip: skip + limit]


@app.post("/authors/", response_model=schemas.Author)
def create_author(
    author: schemas.AuthorCreate,
    db: Session = Depends(get_db)
):
    return crud.create_author(db=db, author=author)


@app.get("/authors/{author_id}/", response_model=schemas.Author)
def read_single_author(
        author_id: int,
        db: Session = Depends(get_db)
):
    data_base_author = crud.get_author_by_id(db=db, author_id=author_id)

    if data_base_author is None:
        raise HTTPException(status_code=404, detail="Author not found")

    return data_base_author


@app.get("/books/", response_model=list[schemas.Book])
def get_all_books(
        skip: int = Query(0, alias="skip"),
        limit: int = Query(10, alias="limit"),
        author_id: int = Query(None, alias="author_id"),
        db: Session = Depends(get_db)
):
    books = crud.get_all_books(db, author_id)

    return books[skip: skip + limit]


@app.get("/books/book_id/", response_model=schemas.Book)
def read_single_book(book_id: int, db: Session = Depends(get_db)):
    data_base_book = crud.get_book_by_id(db=db, book_id=book_id)

    if data_base_book is None:
        raise HTTPException(status_code=404, detail="Book not found")

    return data_base_book


@app.post("/authors/{author_id}/books/", response_model=schemas.Book)
def create_book_for_author(
        author_id: int,
        book: schemas.BookCreate,
        db: Session = Depends(get_db)):
    return crud.create_book(db, book, author_id)
