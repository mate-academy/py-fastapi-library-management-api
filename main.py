from typing import Annotated

from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

import schemas
import crud
from database import get_db_session, Base, engine

Base.metadata.create_all(bind=engine)
app = FastAPI()


@app.get("/authors/", response_model=list[schemas.AuthorRead])
def read_authors(
        db: Annotated[Session, Depends(get_db_session)],
        skip: int = 0,
        limit: int = 100
):
    return crud.get_authors(db=db, skip=skip, limit=limit)


@app.post("/authors/", response_model=schemas.AuthorRead)
def create_author(
        author: schemas.AuthorCreate,
        db: Annotated[Session, Depends(get_db_session)]
):
    author_from_db = crud.get_author_by_name(db=db, author_name=author.name)
    if author_from_db is not None:
        raise HTTPException(status_code=409, detail="Author already exists")
    return crud.create_author(db, author)


@app.get("/authors/{author_id}/", response_model=schemas.AuthorRead)
def get_author(
        author_id: int,
        db_session: Annotated[Session, Depends(get_db_session)]
):
    author_from_db = crud.get_author_by_id(db=db_session, author_id=author_id)
    if author_from_db is None:
        raise HTTPException(status_code=404, detail="Author not found")
    return author_from_db


@app.post("/authors/{author_id}/books/", response_model=schemas.BookRead, status_code=201)
def create_book(
        db_session: Annotated[Session, Depends(get_db_session)],
        book: schemas.BookCreate,
        author_id: int
):
    author_from_db = crud.get_author_by_id(db=db_session, author_id=author_id)
    if author_from_db is None:
        raise HTTPException(status_code=404, detail="Author not found")
    return crud.create_book(db=db_session, book=book, author_id=author_id)


@app.get("/books/", response_model=list[schemas.BookRead])
def get_books(
        db_session: Annotated[Session, Depends(get_db_session)],
        skip: int = 0,
        limit: int = 100,
        author_id: int | None = None
):
    return crud.get_books(db=db_session, skip=skip, limit=limit, author_id=author_id)
