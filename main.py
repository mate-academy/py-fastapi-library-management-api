from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException, Query, status
from sqlalchemy.orm import Session

import crud
import models
import schemas
from database import engine, get_db


models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Library Management API",
    description="A simple API for managing authors and their books.",
    version="1.0.0",
)

DbSession = Annotated[Session, Depends(get_db)]


@app.post(
    "/authors/",
    response_model=schemas.Author,
    status_code=status.HTTP_201_CREATED,
)
def create_author(author: schemas.AuthorCreate, db: DbSession) -> models.Author:
    if crud.get_author_by_name(db, author.name) is not None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="An author with this name already exists",
        )
    return crud.create_author(db=db, author=author)


@app.get("/authors/", response_model=list[schemas.Author])
def read_authors(
    db: DbSession,
    skip: Annotated[int, Query(ge=0)] = 0,
    limit: Annotated[int, Query(ge=1, le=100)] = 100,
) -> list[models.Author]:
    return crud.get_authors(db=db, skip=skip, limit=limit)


@app.get("/authors/{author_id}", response_model=schemas.Author)
def read_author(author_id: int, db: DbSession) -> models.Author:
    author = crud.get_author(db, author_id)
    if author is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Author not found",
        )
    return author


@app.post(
    "/authors/{author_id}/books/",
    response_model=schemas.Book,
    status_code=status.HTTP_201_CREATED,
)
def create_book_for_author(
    author_id: int,
    book: schemas.BookCreate,
    db: DbSession,
) -> models.Book:
    if crud.get_author(db, author_id) is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Author not found",
        )
    return crud.create_book(db=db, book=book, author_id=author_id)


@app.get("/books/", response_model=list[schemas.Book])
def read_books(
    db: DbSession,
    skip: Annotated[int, Query(ge=0)] = 0,
    limit: Annotated[int, Query(ge=1, le=100)] = 100,
    author_id: Annotated[int | None, Query(ge=1)] = None,
) -> list[models.Book]:
    return crud.get_books(
        db=db,
        skip=skip,
        limit=limit,
        author_id=author_id,
    )
