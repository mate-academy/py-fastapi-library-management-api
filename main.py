from typing import List

from fastapi import FastAPI, Depends, HTTPException, Query
from sqlalchemy.orm import Session

import crud
import models
import schemas
from database import SessionLocal


app = FastAPI()


def get_db() -> Session:
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()


@app.get("/authors/", response_model=List[schemas.Author])
def read_authors(
        skip: int = Query(0),
        limit: int = Query(10),
        db: Session = Depends(get_db),
) -> List[models.Author]:

    authors = crud.get_authors_with_pagination(db=db, skip=skip, limit=limit)

    return authors


@app.get("/authors/{author_id}/", response_model=schemas.Author)
def retrieve_author_by_id(
        author_id: int,
        db: Session = Depends(get_db)
) -> models.Author:

    db_author = crud.get_author_by_id(author_id=author_id, db=db)

    if db_author is None:
        raise HTTPException(status_code=404, detail="Author not found")

    return db_author


@app.post("/authors/", response_model=schemas.Author)
def create_author(
        author: schemas.AuthorCreate,
        db: Session = Depends(get_db)
) -> models.Author:

    db_author = crud.get_author_by_name(db=db, name=author.name)

    if db_author:
        raise HTTPException(
            status_code=400,
            detail="Such name for Author already exists"
        )

    return crud.create_author(db=db, author=author)


@app.get("/books/", response_model=List[schemas.Book])
def read_books(
        skip: int = Query(0),
        limit: int = Query(10),
        author_id: int | None = None,
        db: Session = Depends(get_db),
) -> List[models.Book]:

    books = crud.get_books_with_pagination(
        db=db, author_id=author_id, skip=skip, limit=limit
    )

    return books


@app.post("/books/", response_model=schemas.Book)
def create_book(
        book: schemas.BookCreate,
        db: Session = Depends(get_db),
) -> models.Book:

    return crud.create_book(db=db, book=book)
