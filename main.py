from fastapi import FastAPI, Depends, HTTPException
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


@app.get("/")
def read_root():
    return {"test": "test"}


@app.get("/authors/", response_model=list[schemas.Author])
def read_authors(
    offset: int = None,
    limit: int = None,
    db: Session = Depends(get_db)
) -> [schemas.Author]:
    return crud.get_authors_list(
        db,
        offset=offset,
        limit=limit
    )


@app.get("/authors/{author_id}", response_model=schemas.Author)
def read_author(author_id: int, db: Session = Depends(get_db)):
    author = crud.get_single_author(db, author_id)
    if not author:
        raise HTTPException(status_code=404, detail="Author not found")
    return author


@app.post("/authors/", response_model=schemas.Author)
def create_author(
    author: schemas.AuthorCreate,
    db: Session = Depends(get_db),
) -> schemas.Author:
    return crud.create_author(db, author)


@app.get("/books/", response_model=list[schemas.Book])
def read_books(
    offset: int = None,
    limit: int = None,
    author_id: int = None,
    db: Session = Depends(get_db)
) -> [schemas.Book]:
    return crud.get_books_list(
        db,
        offset=offset,
        limit=limit,
        author_id=author_id
    )


@app.get("/books/{book_id}", response_model=schemas.Book)
def read_single_book(
    book_id: int,
    db: Session = Depends(get_db)
) -> schemas.Book:
    book = crud.get_single_book(db, book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return book


@app.post("/books/", response_model=schemas.Book)
def create_book(
    book: schemas.BookCreate,
    db: Session = Depends(get_db),
) -> schemas.Book:
    return crud.create_book(db, book)
