from typing import Annotated

from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

import schemas
import crud
from database import get_db

app = FastAPI()
DbDep = Annotated[Session, Depends(get_db)]


@app.get("/")
def read_root() -> dict:
    return {"Hello": "World"}


@app.get("/authors/", response_model=list[schemas.AuthorRead])
def read_authors(db: DbDep, skip: int = 0, limit: int = 10):
    return crud.get_authors(db=db, skip=skip, limit=limit)


@app.get("/authors/{author_id}/", response_model=schemas.AuthorRead)
def read_author(author_id: int, db: DbDep):
    author = crud.get_author(db=db, author_id=author_id)
    if author is None:
        raise HTTPException(status_code=404, detail="No author with such id exists")
    return author


@app.post("/authors/", response_model=schemas.AuthorRead, status_code=201)
def create_author(data: schemas.AuthorCreate, db: DbDep):
    author = crud.get_author_by_name(db=db, name=data.name)
    if author:
        raise HTTPException(
            status_code=400, detail="An author with this name already exists"
        )
    return crud.create_author(db=db, data=data)


@app.get("/books/", response_model=list[schemas.BookRead])
def read_books(db: DbDep, author_id: int | None = None, skip: int = 0, limit: int = 10):
    if author_id is not None and crud.get_author(db=db, author_id=author_id) is None:
        raise HTTPException(status_code=404, detail="No author with such id exists")
    return crud.get_books(db=db, author_id=author_id, skip=skip, limit=limit)


@app.get("/books/{book_id}/", response_model=schemas.BookRead)
def read_book(db: DbDep, book_id: int):
    book = crud.get_book(db=db, book_id=book_id)
    if book is None:
        raise HTTPException(status_code=404, detail="No book with such id exists")
    return book


@app.post("/books/", response_model=schemas.BookRead, status_code=201)
def create_book(data: schemas.BookCreate, db: DbDep):
    book = crud.create_book(db=db, data=data)
    if book is None:
        raise HTTPException(
            status_code=400, detail="The chosen author for this book does not exist"
        )
    return book
