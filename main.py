from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException, Query, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

import crud
import models  # noqa: F401 - register models before creating tables
import schemas
from database import Base, SessionLocal, engine


Base.metadata.create_all(bind=engine)
app = FastAPI(title="Library Management API")


def get_db():
    with SessionLocal() as db:
        yield db


DbSession = Annotated[Session, Depends(get_db)]


@app.post("/authors/", response_model=schemas.AuthorRead, status_code=201)
def create_author(author: schemas.AuthorCreate, db: DbSession):
    if crud.get_author_by_name(db, author.name):
        raise HTTPException(
            status_code=400, detail="Author name already exists"
        )
    try:
        return crud.create_author(db, author)
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=400, detail="Author name already exists"
        )


@app.get("/authors/", response_model=list[schemas.AuthorRead])
def list_authors(db: DbSession, skip: int = Query(0, ge=0),
                 limit: int = Query(100, ge=1)):
    return crud.get_authors(db, skip, limit)


@app.get("/authors/{author_id}", response_model=schemas.AuthorRead)
def read_author(author_id: int, db: DbSession):
    author = crud.get_author(db, author_id)
    if author is None:
        raise HTTPException(status_code=404, detail="Author not found")
    return author


@app.post("/authors/{author_id}/books/", response_model=schemas.BookRead,
          status_code=status.HTTP_201_CREATED)
def create_author_book(
    author_id: int, book: schemas.BookCreate, db: DbSession
):
    if crud.get_author(db, author_id) is None:
        raise HTTPException(status_code=404, detail="Author not found")
    return crud.create_book(db, book, author_id)


@app.get("/books/", response_model=list[schemas.BookRead])
def list_books(db: DbSession, skip: int = Query(0, ge=0),
               limit: int = Query(100, ge=1), author_id: int | None = None):
    return crud.get_books(db, skip, limit, author_id)
