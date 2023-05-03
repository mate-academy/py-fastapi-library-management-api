from http.client import HTTPException

from fastapi import FastAPI, Depends

import crud
import schemas

from database import SessionLocal

app = FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/authors/", response_model=schemas.Author)
def create_author(author: schemas.AuthorCreate, db: SessionLocal = Depends(get_db)):
    return crud.create_author(db=db, author=author)


@app.get("/authors/", response_model=list[schemas.Author])
def read_authors(skip: int = 0, limit: int = 100, db: SessionLocal = Depends(get_db)):
    authors = crud.get_all_authors(db, skip=skip, limit=limit)
    return authors


@app.get("/authors/{author_id}", response_model=schemas.Author)
def read_author(author_id: int, db: SessionLocal = Depends(get_db)):
    db_author = crud.get_author_by_id(db, author_id=author_id)
    if db_author is None:
        raise HTTPException(
            "Author not found",
        )
    return db_author


@app.post("/books/", response_model=schemas.Book)
def create_book(book: schemas.BookCreate, db: SessionLocal = Depends(get_db)):
    return crud.create_book(db=db, book=book)


@app.get("/books/", response_model=list[schemas.Book])
def read_books(skip: int = 0, limit: int = 100, db: SessionLocal = Depends(get_db)):
    books = crud.get_all_books(db, skip=skip, limit=limit)
    return books


@app.get("/books/{book_id}", response_model=schemas.Book)
def read_book(book_id: int, db: SessionLocal = Depends(get_db)):
    db_book = crud.get_book_by_id(db, book_id=book_id)
    if db_book is None:
        raise HTTPException(
            "Book not found",
        )
    return db_book


@app.get("/books/filter/{author_id}/", response_model=list[schemas.Book])
def filter_books_by_author(author_id: int, db: SessionLocal = Depends(get_db)):
    books = crud.filter_books_by_author(db, author_id=author_id)
    return books
