from typing import List

from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session

import crud
from db.engine import SessionLocal
from schemas import Author, Book


app = FastAPI()


def get_db() -> Session:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
def read_root() -> dict:
    return {"Hello": "World"}


@app.get("authors/", response_model=List[Author])
def read_authors(
        db: Session = Depends(get_db),
        skip: int = 0,
        limit: int = 100
) -> List[Author]:
    authors = crud.get_all_authors(db, skip=skip, limit=limit)
    return authors


@app.get("authors/{author_id}", response_model=Author)
def read_author(author_id: int, db: Session = Depends(get_db)) -> Author:
    author = crud.get_single_author(db, author_id)
    return author


@app.post("authors/", response_model=Author)
def create_author(author: Author, db: Session = Depends(get_db)) -> Author:
    return crud.create_author(db=db, name=author.name, bio=author.bio)


@app.get("books/", response_model=List[Author])
def read_books(
        db: Session = Depends(get_db),
        skip: int = 0, limit:
        int = 100
) -> List[Book]:
    books = crud.get_all_books(db=db, skip=skip, limit=limit)
    return books


@app.get("books/{author_id}", response_model=List[Author])
def read_books_by_author_id(
        author_id: int,
        db: Session = Depends(get_db)
) -> List[Book]:
    books = crud.get_books_by_author_id(db=db, author_id=author_id)
    return books


@app.post("books/", response_model=Author)
def create_book(book: Author, db: Session = Depends(get_db)) -> Author:
    return crud.create_book(
        db=db,
        title=book.title,
        summary=book.summary,
        publication_date=book.publication_date,
        author_id=book.author_id
    )
