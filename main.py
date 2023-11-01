from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

import schemas
import crud
from db.database import SessionLocal

app = FastAPI()


def get_db() -> Session:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/authors/", response_model=list[schemas.AuthorList])
def read_authors(
    skip: int = 0, limit: int = 10, db: Session = Depends(get_db)
):
    authors = crud.get_all_authors(db, skip, limit)
    return authors


@app.post("/authors/", response_model=schemas.AuthorCreate)
def create_author(author: schemas.AuthorCreate, db: Session = Depends(get_db)):
    return crud.create_author(db=db, author=author)


@app.get("/authors/{author_id}", response_model=schemas.AuthorList)
def read_author(author_id: int, db: Session = Depends(get_db)):
    db_author = crud.get_author_by_id(db=db, author_id=author_id)
    if db_author is None:
        raise HTTPException(status_code=404, detail="Author not found")
    return db_author


@app.get("/books/", response_model=list[schemas.BookList])
def read_books(
    skip: int = 0,
    limit: int = 10,
    author_id: int = None,
    db: Session = Depends(get_db),
):
    books = crud.get_all_books(
        db=db, author_id=author_id, skip=skip, limit=limit
    )
    return books


@app.post("/books/", response_model=schemas.BookCreate)
def create_book(book: schemas.BookCreate, db: Session = Depends(get_db)):
    return crud.create_book(db=db, book=book)


@app.get("/books/{book_id}", response_model=schemas.BookList)
def read_book(book_id: int, db: Session = Depends(get_db)):
    db_book = crud.get_book_by_id(db=db, book_id=book_id)
    if db_book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    return db_book
