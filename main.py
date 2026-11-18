from typing import Annotated, Generator

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

import crud
import models
import schemas

from database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()


@app.get("/authors/", response_model=list[schemas.Author])
def read_authors(
    db: Annotated[Session, Depends(get_db)],
    skip: int = 0,
    limit: int = 10
):
    if skip < 0:
        raise HTTPException(
            status_code=400,
            detail="skip must be greater than or equal to 0."
        )
    if not (1 <= limit <= 100):
        raise HTTPException(
            status_code=400,
            detail="limit cannot be less than 1 or greater than 100."
        )

    return crud.get_all_authors(db=db, skip=skip, limit=limit)


@app.post("/authors/", response_model=schemas.Author)
def create_author(
    author: schemas.AuthorCreate,
    db: Annotated[Session, Depends(get_db)]
):
    db_author = crud.get_author_by_name(db=db, name=author.name)

    if db_author:
        raise HTTPException(
            status_code=400,
            detail="An author with this name already exists."
        )

    return crud.create_author(db=db, author=author)


@app.get("/authors/{author_id}/", response_model=schemas.Author)
def read_single_author(
    author_id: int,
    db: Annotated[Session, Depends(get_db)]
):
    db_author = crud.get_author_by_id(db=db, author_id=author_id)

    if not db_author:
        raise HTTPException(status_code=404, detail="Author not found")

    return db_author


@app.get("/books/", response_model=list[schemas.Book])
def read_books(
    db: Annotated[Session, Depends(get_db)],
    author_id: int | None = None,
    skip: int = 0,
    limit: int = 10
):
    if skip < 0:
        raise HTTPException(
            status_code=400,
            detail="skip must be greater than or equal to 0."
        )
    if not (1 <= limit <= 100):
        raise HTTPException(
            status_code=400,
            detail="limit cannot be less than 1 or greater than 100."
        )

    return crud.get_all_books(
        db=db,
        author_id=author_id,
        skip=skip,
        limit=limit
    )


@app.post("/books/", response_model=schemas.Book)
def create_book(
    book: schemas.BookCreate,
    db: Annotated[Session, Depends(get_db)]
):
    db_author = crud.get_author_by_id(db=db, author_id=book.author_id)

    if not db_author:
        raise HTTPException(status_code=404, detail="Author not found")

    return crud.create_book(db=db, book=book)
