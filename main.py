from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException, Query, status
from sqlalchemy.orm import Session

import models
import schemas
from crud import crud
from db.database import Base, SessionLocal, engine


Base.metadata.create_all(bind=engine)

app = FastAPI(title="Library Management API")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


DbSession = Annotated[Session, Depends(get_db)]
PaginationSkip = Annotated[int, Query(ge=0)]
PaginationLimit = Annotated[int, Query(ge=1, le=100)]


@app.post(
    "/authors/",
    response_model=schemas.Author,
    status_code=status.HTTP_201_CREATED,
)
def create_author(author: schemas.AuthorCreate, db: DbSession):
    db_author = crud.get_author_by_name(db, name=author.name)
    if db_author:
        raise HTTPException(status_code=400, detail="Author name already registered")

    return crud.create_author(db=db, author=author)


@app.get("/authors/", response_model=list[schemas.Author])
def read_authors(
    db: DbSession,
    skip: PaginationSkip = 0,
    limit: PaginationLimit = 100,
):
    return crud.get_authors(db, skip=skip, limit=limit)


@app.get("/authors/{author_id}", response_model=schemas.Author)
def read_author(author_id: int, db: DbSession):
    db_author = crud.get_author(db, author_id=author_id)
    if db_author is None:
        raise HTTPException(status_code=404, detail="Author not found")

    return db_author


@app.post(
    "/authors/{author_id}/books/",
    response_model=schemas.Book,
    status_code=status.HTTP_201_CREATED,
)
def create_book_for_author(
    author_id: int,
    book: schemas.BookCreate,
    db: DbSession,
):
    db_author = crud.get_author(db, author_id=author_id)
    if db_author is None:
        raise HTTPException(status_code=404, detail="Author not found")

    return crud.create_book(db=db, book=book, author_id=author_id)


@app.get("/books/", response_model=list[schemas.Book])
def read_books(
    db: DbSession,
    skip: PaginationSkip = 0,
    limit: PaginationLimit = 100,
    author_id: Annotated[int | None, Query(ge=1)] = None,
):
    if author_id is not None:
        db_author = crud.get_author(db, author_id=author_id)
        if db_author is None:
            raise HTTPException(status_code=404, detail="Author not found")

        return crud.get_books_by_author(db, author_id=author_id, skip=skip, limit=limit)

    return crud.get_books(db, skip=skip, limit=limit)


@app.get("/books/by-author/{author_id}", response_model=list[schemas.Book])
def read_books_by_author(
    author_id: int,
    db: DbSession,
    skip: PaginationSkip = 0,
    limit: PaginationLimit = 100,
):
    db_author = crud.get_author(db, author_id=author_id)
    if db_author is None:
        raise HTTPException(status_code=404, detail="Author not found")

    return crud.get_books_by_author(db, author_id=author_id, skip=skip, limit=limit)
