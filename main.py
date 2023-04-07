from typing import Optional

from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

import schemas
from crud import Library
from database import SessionLocal

app = FastAPI()


def get_db() -> Session:
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()


@app.post("/authors/", response_model=schemas.Author)
def create_author(
        author: schemas.AuthorCreate,
        db: Session = Depends(get_db)
) -> schemas.Author:
    library = Library(db)
    db_author = library.get_author_by_name(name=author.name)
    if db_author:
        raise HTTPException(
            status_code=400,
            detail="Author name already exists"
        )
    return library.create_author(author=author)


@app.get("/authors/", response_model=list[schemas.Author])
def read_authors(
        skip: int = 0,
        limit: int = 100,
        db: Session = Depends(get_db)
) -> list[schemas.Author]:
    library = Library(db)
    authors = library.get_author_list(skip=skip, limit=limit)
    return authors


@app.get("/authors/{author_id}/", response_model=schemas.Author)
def read_single_author(
        author_id: int,
        db: Session = Depends(get_db)
) -> Optional[schemas.Author]:
    library = Library(db)
    db_author = library.get_author(author_id=author_id)
    if db_author is None:
        raise HTTPException(status_code=404, detail="Author not found")
    return db_author


@app.post("/books/", response_model=schemas.Book)
def create_book(
        book: schemas.BookCreate,
        db: Session = Depends(get_db),
) -> schemas.Book:
    library = Library(db)
    author = library.get_author(author_id=book.author_id)
    if author is None:
        raise HTTPException(status_code=404, detail="Author not found")
    return library.create_book(book=book)


@app.get("/books/", response_model=list[schemas.Book])
def read_books(
        skip: int = 0,
        limit: int = 100,
        db: Session = Depends(get_db)
) -> list[schemas.Author]:
    library = Library(db)
    books = library.get_book_list(skip=skip, limit=limit)
    return books


@app.get("/books/author/{author_id}", response_model=list[schemas.Book])
def read_books_by_author(
    author_id: int,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
) -> list[schemas.Book]:
    library = Library(db)
    books = library.get_books_by_author(
        author_id=author_id,
        skip=skip,
        limit=limit
    )
    if not books:
        raise HTTPException(status_code=404, detail="Author has no books")
    return books
