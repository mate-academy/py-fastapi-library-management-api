from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException, Query, status
from sqlalchemy.orm import Session

import crud
from database import SessionLocal, engine
from models import Base
from schemas import (
    AuthorCreate,
    AuthorOut,
    AuthorOutWithBooks,
    BookCreate,
    BookOut,
)


Base.metadata.create_all(bind=engine)


app = FastAPI(title="Library Management API")


def get_db():
    with SessionLocal() as db:
        yield db


DBSession = Annotated[Session, Depends(get_db)]


@app.get("/")
def root():
    return {"status": "ok"}


@app.post(
    "/authors",
    response_model=AuthorOut,
    status_code=status.HTTP_201_CREATED,
)
def create_author(author_in: AuthorCreate, db: DBSession):
    existing = crud.get_author_by_name(db, author_in.name)
    if existing:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Author with this name already exists",
        )
    return crud.create_author(db, author_in)


@app.get("/authors", response_model=list[AuthorOut])
def list_authors(
    db: DBSession,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
):
    return crud.get_authors(db, skip=skip, limit=limit)


@app.get("/authors/{author_id}", response_model=AuthorOutWithBooks)
def get_author(author_id: int, db: DBSession):
    author = crud.get_author_with_books(db, author_id)
    if not author:
        raise HTTPException(status_code=404, detail="Author not found")
    return author


@app.post(
    "/authors/{author_id}/books",
    response_model=BookOut,
    status_code=status.HTTP_201_CREATED,
)
def create_book_for_author(author_id: int, book_in: BookCreate, db: DBSession):
    author = crud.get_author_by_id(db, author_id)
    if not author:
        raise HTTPException(status_code=404, detail="Author not found")
    return crud.create_book_for_author(db, author_id=author_id, book_in=book_in)


@app.get("/books", response_model=list[BookOut])
def list_books(
    db: DBSession,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    author_id: int | None = Query(default=None, ge=1),
):
    return crud.get_books(db, skip=skip, limit=limit, author_id=author_id)
