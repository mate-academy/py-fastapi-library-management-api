from typing import Annotated, Generator

from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

import crud
import models  # noqa: F401
import schemas
from database import SessionLocal, engine, Base

Base.metadata.create_all(bind=engine)

app = FastAPI()


def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()


@app.post("/author/", response_model=schemas.Author)
def create_author(
    author: schemas.AuthorCreate,
    db: Annotated[Session, Depends(get_db)],
):
    db_author = crud.get_author_by_name(db=db, name=author.name)
    if db_author:
        raise HTTPException(
            status_code=400,
            detail="Author with this name already exists",
        )

    return crud.create_author(db=db, author=author)


@app.get("/authors/", response_model=list[schemas.Author])
def read_authors(
    db: Annotated[Session, Depends(get_db)],
    skip: int = 0,
    limit: int = 100,
):
    return crud.get_authors_list(db=db, skip=skip, limit=limit)


@app.get("/authors/{author_id}/", response_model=schemas.Author)
def read_author_by_id(
    author_id: int,
    db: Annotated[Session, Depends(get_db)],
):
    db_author = crud.get_author_by_id(db=db, author_id=author_id)
    if not db_author:
        raise HTTPException(status_code=404, detail="Author not found")

    return db_author


@app.post("/authors/{author_id}/books/", response_model=schemas.Book)
def create_book(
    author_id: int,
    book: schemas.BookCreate,
    db: Annotated[Session, Depends(get_db)],
):
    db_author = crud.get_author_by_id(db=db, author_id=author_id)
    if not db_author:
        raise HTTPException(status_code=404, detail="Author not found")

    return crud.create_book(db=db, book=book, author_id=author_id)


@app.get("/books/", response_model=list[schemas.Book])
def read_books(
    db: Annotated[Session, Depends(get_db)],
    author_id: int | None = None,
    skip: int = 0,
    limit: int = 100,
):
    return crud.get_books_list(
        db=db, author_id=author_id, skip=skip, limit=limit
    )
