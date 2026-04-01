from typing import Annotated

from fastapi import FastAPI, Depends, Query, status, HTTPException
from sqlalchemy.orm import Session

import crud
import models
import schemas
from crud import AuthorAlreadyExists, AuthorNotFound
from database import engine, get_db

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Library Management API")


DbSession = Annotated[Session, Depends(get_db)]
PaginationSkip = Annotated[int, Query(ge=0, description="Records to skip")]
PaginationLimit = Annotated[
    int, Query(ge=1, le=100, description="Max records to return")
]


@app.post(
    "/authors/",
    response_model=schemas.AuthorResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_author(
    author: schemas.AuthorCreate, db: DbSession
) -> schemas.AuthorResponse:
    try:
        return crud.create_author(db=db, author=author)
    except AuthorAlreadyExists:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Author with that name already exists",
        )


@app.get("/authors/", response_model=list[schemas.AuthorResponse])
def read_authors(
    db: DbSession, skip: PaginationSkip = 0, limit: PaginationLimit = 10
) -> list[schemas.AuthorResponse]:
    return crud.get_authors(db=db, skip=skip, limit=limit)


@app.get("/authors/{author_id}", response_model=schemas.AuthorDetailResponse)
def read_author(db: DbSession, author_id: int) -> schemas.AuthorDetailResponse:
    db_author = crud.get_author(db=db, author_id=author_id)
    if db_author is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Author not found"
        )
    return db_author


@app.post(
    "/books/",
    response_model=schemas.BookResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_book(db: DbSession, book: schemas.BookCreate) -> schemas.BookResponse:
    try:
        return crud.create_book(db=db, book=book)
    except AuthorNotFound:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Author with that id not found",
        )


@app.get("/books/", response_model=list[schemas.BookResponse])
def read_books(
    db: DbSession,
    skip: PaginationSkip = 0,
    limit: PaginationLimit = 10,
    author_id: Annotated[
        int | None, Query(ge=1, description="Filter books by author ID")
    ] = None,
) -> list[schemas.BookResponse]:
    return crud.get_books(db=db, skip=skip, limit=limit, author_id=author_id)
