from typing import Annotated, Generator

from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

import crud
import schemas
from database import Base, SessionLocal, engine


Base.metadata.create_all(bind=engine)
app = FastAPI()


def get_database() -> Generator[Session, None, None]:
    database = SessionLocal()

    try:
        yield database
    finally:
        database.close()


@app.get("/authors/", response_model=list[schemas.AuthorRead])
def read_authors(
        database: Annotated[Session, Depends(get_database)],
        skip: int = 0,
        limit: int = 100,
):
    return crud.get_all_authors(database=database, skip=skip, limit=limit)


@app.get("/authors/{author_id}/", response_model=schemas.AuthorRead)
def read_single_author(
        author_id: int,
        database: Annotated[Session, Depends(get_database)]
):
    database_author = crud.get_author_by_id(
        database=database,
        author_id=author_id
    )

    if not database_author:
        raise HTTPException(
            status_code=404,
            detail="Author not found"
        )

    return database_author


@app.post("/authors/", response_model=schemas.AuthorRead, status_code=201)
def create_author(
        author: schemas.AuthorCreate,
        database: Annotated[Session, Depends(get_database)],
):
    database_author = crud.get_author_by_name(
        database=database,
        name=author.name
    )

    if database_author:
        raise HTTPException(
            status_code=400,
            detail="Author already exists"
        )

    return crud.create_author(database=database, author=author)


@app.get("/books/", response_model=list[schemas.BookRead])
def read_books(
        database: Annotated[Session, Depends(get_database)],
        skip: int = 0,
        limit: int = 100,
        author_id: int | None = None,
):
    return crud.get_all_books(
        database=database,
        skip=skip,
        limit=limit,
        author_id=author_id,
    )


@app.get("/books/{book_id}/", response_model=schemas.BookRead)
def read_single_book(
        book_id: int,
        database: Annotated[Session, Depends(get_database)]
):
    database_book = crud.get_book_by_id(
        database=database,
        book_id=book_id
    )

    if not database_book:
        raise HTTPException(
            status_code=404,
            detail="Book not found"
        )

    return database_book


@app.post(
    "/authors/{author_id}/books/",
    response_model=schemas.BookRead,
    status_code=201,
)
def create_book(
        author_id: int,
        book: schemas.BookCreate,
        database: Annotated[Session, Depends(get_database)],
):
    database_author = crud.get_author_by_id(
        database=database,
        author_id=author_id
    )

    if not database_author:
        raise HTTPException(
            status_code=404,
            detail="Author not found"
        )

    return crud.create_book(
        database=database,
        book=book,
        author_id=author_id,
    )
