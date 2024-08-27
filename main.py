from typing import List

from fastapi import (
    Depends,
    FastAPI,
    HTTPException,
    Query,
)
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
def root() -> dict[str, str]:
    return {"message": "Welcome to Library!"}


@app.get("/authors/", response_model=List[schemas.Author])
def read_authors_list(
    skip: int = Query(0, ge=0),
    limit: int = Query(2, ge=1),
    db: Session = Depends(get_db)
) -> list[schemas.Author]:
    authors = crud.get_author_list(db, skip=skip, limit=limit)
    return authors


@app.get("/authors/{author_id}", response_model=schemas.Author)
def read_author_by_id(
        author_id: int,
        db: Session = Depends(get_db)
) -> schemas.Author:
    author = crud.get_author_by_id(db, author_id)

    if author is None:
        raise HTTPException(status_code=404, detail="Author not found")
    return author


@app.post("/authors/", response_model=schemas.Author)
def create_author(
        author: schemas.AuthorCreate,
        db: Session = Depends(get_db)
) -> schemas.Author:
    db_author = crud.get_author_by_name(db=db, name=author.name)

    if db_author:
        raise HTTPException(
            status_code=400,
            detail="Author with this name already exists"
        )

    return crud.create_author(db=db, author=author)


@app.get("/books/", response_model=List[schemas.Book])
def read_book_list(
        skip: int = 0,
        limit: int = 2,
        db: Session = Depends(get_db)
) -> list[schemas.Book]:
    return crud.get_books_list(db=db, skip=skip, limit=limit)


@app.get("/books/{author_id}/", response_model=list[schemas.Book])
def get_single_book(
        author_id: int,
        db: Session = Depends(get_db)
) -> list[schemas.Book]:
    db_books = crud.get_books_by_author_id(author_id=author_id, db=db)

    if db_books is None:
        raise HTTPException(
            status_code=404,
            detail="Books not found"
        )

    return db_books


@app.post("/books/", response_model=schemas.Book)
def create_book(
        book: schemas.BookCreate,
        db: Session = Depends(get_db)
) -> schemas.Book:

    return crud.create_book(db=db, book=book)
