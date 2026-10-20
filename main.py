from contextlib import asynccontextmanager
from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException, Query, status
from sqlalchemy.orm import Session

import crud
import models
import schemas
from database import Base, SessionLocal, engine


@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(
    title="Library Management API",
    lifespan=lifespan,
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


DbSession = Annotated[Session, Depends(get_db)]


@app.post(
    "/authors/",
    response_model=schemas.Author,
    status_code=status.HTTP_201_CREATED,
)
def create_author(
    author: schemas.AuthorCreate,
    db: DbSession,
):
    existing_author = crud.get_author_by_name(
        db=db,
        name=author.name,
    )

    if existing_author:
        raise HTTPException(
            status_code=400,
            detail="Author with this name already exists",
        )

    return crud.create_author(db=db, author=author)


@app.get(
    "/authors/",
    response_model=list[schemas.Author],
)
def read_authors(
    db: DbSession,
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=100, ge=1),
):
    return crud.get_authors(
        db=db,
        skip=skip,
        limit=limit,
    )


@app.get(
    "/authors/{author_id}",
    response_model=schemas.Author,
)
def read_author(
    author_id: int,
    db: DbSession,
):
    author = crud.get_author(
        db=db,
        author_id=author_id,
    )

    if author is None:
        raise HTTPException(
            status_code=404,
            detail="Author not found",
        )

    return author


@app.post(
    "/authors/{author_id}/books/",
    response_model=schemas.Book,
    status_code=status.HTTP_201_CREATED,
)
def create_book(
    author_id: int,
    book: schemas.BookCreate,
    db: DbSession,
):
    author = crud.get_author(
        db=db,
        author_id=author_id,
    )

    if author is None:
        raise HTTPException(
            status_code=404,
            detail="Author not found",
        )

    return crud.create_book(
        db=db,
        book=book,
        author_id=author_id,
    )


@app.get(
    "/books/",
    response_model=list[schemas.Book],
)
def read_books(
    db: DbSession,
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=100, ge=1),
    author_id: int | None = Query(default=None, ge=1),
):
    return crud.get_books(
        db=db,
        skip=skip,
        limit=limit,
        author_id=author_id,
    )
