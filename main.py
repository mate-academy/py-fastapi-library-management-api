from typing import Sequence, Generator

from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

import models
import schemas
import crud
from database import SessionLocal, engine


models.Base.metadata.create_all(bind=engine)
app = FastAPI(title="Library Management API")


def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/authors/", response_model=schemas.AuthorRead)
def create_author(
        author: schemas.AuthorCreate,
        db: Session = Depends(get_db)
) -> models.Author:

    return crud.create_author(db, author)


@app.get("/authors/", response_model=list[schemas.AuthorRead])
def list_authors(
        skip: int = 0,
        limit: int = 10,
        db: Session = Depends(get_db)
) -> Sequence[models.Author]:

    return crud.get_all_authors(db, skip=skip, limit=limit)


@app.get("/authors/{author_id}", response_model=schemas.AuthorRead)
def get_author(
        author_id: int,
        db: Session = Depends(get_db)
) -> models.Author:
    author = crud.get_author_by_id(db, author_id)
    if not author:
        raise HTTPException(status_code=404, detail="Author not found")

    return author


@app.post("/authors/{author_id}/books/", response_model=schemas.BookRead)
def create_book(
        author_id: int,
        book: schemas.BookCreate,
        db: Session = Depends(get_db)
) -> models.Book | None:
    if not crud.get_author_by_id(db, author_id):
        raise HTTPException(status_code=404, detail="Author not found")

    return crud.create_book(db, book, author_id)


@app.get("/books/", response_model=list[schemas.BookRead])
def books_by_author(
        author_id: int | None = None,
        skip: int = 0,
        limit: int = 10,
        db: Session = Depends(get_db)
) -> Sequence[models.Book]:
    if author_id:
        return crud.get_books_by_author(
            db,
            author_id=author_id,
            skip=skip,
            limit=limit
        )

    return crud.get_all_books(db, skip=skip, limit=limit)
