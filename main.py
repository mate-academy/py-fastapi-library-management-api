from typing import List

from fastapi import FastAPI, Depends, HTTPException, Query

from sqlalchemy.orm import Session

import crud
from database import SessionLocal
from schemas import Author, AuthorCreate, Book, BookCreate

app = FastAPI()


def get_db() -> Session:
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()


@app.get("/")
def root():
    return {"message": "Hello World"}


@app.get("/authors/", response_model=List[Author])
def read_authors(
        db: Session = Depends(get_db),
        skip: int = Query(0, ge=0),
        limit: int = Query(3, le=30)
):
    return crud.get_all_authors(db=db, skip=skip, limit=limit)


@app.get("/authors/{author_id}/", response_model=Author)
def read_single_author(author_id: int, db: Session = Depends(get_db)):
    db_author = crud.get_author_by_id(db=db, author_id=author_id)

    if db_author is None:
        raise HTTPException(status_code=404, detail="Author not found")

    return db_author


@app.post("/authors/", response_model=Author)
def create_author(
        author: AuthorCreate,
        db: Session = Depends(get_db),
):
    db_author = crud.get_author_by_name(db=db, name=author.name)

    if db_author:
        raise HTTPException(
            status_code=400,
            detail="Such name for Author already exists"
        )
    return crud.create_author(db=db, author=author)


@app.get("/books/", response_model=List[Book])
def read_books(
        db: Session = Depends(get_db),
        author_id: int | None = None,
        skip: int = Query(0, ge=0),
        limit: int = Query(Query(10)),
):
    return crud.get_book_list(
        db=db,
        author_id=author_id,
        skip=skip,
        limit=limit,
    )


@app.get("/books/{book_id}/", response_model=Book)
def read_single_book(book_id: int, db: Session = Depends(get_db)):
    db_book = crud.get_book(db=db, book_id=book_id)

    if db_book is None:
        raise HTTPException(status_code=404, detail="Book not found")

    return db_book


@app.post("/books/", response_model=Book)
def create_book(book: BookCreate, db: Session = Depends(get_db)):
    return crud.create_book(db=db, book=book)
