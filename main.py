from fastapi import FastAPI, HTTPException, Depends, Query
from sqlalchemy.orm import Session

import schemas
from database import engine
from typing import Annotated

import crud

app = FastAPI()


def get_session():
    with Session(engine) as session:
        yield session


SessionDep = Annotated[Session, Depends(get_session)]


@app.get("/authors/", response_model=list[schemas.Author])
def read_authors(
    db: SessionDep,
    skip: Annotated[int, Query(ge=0)] = 0,
    limit: Annotated[int, Query(ge=1, le=100)] = 10,
):
    return crud.get_author_list(db=db, skip=skip, limit=limit)


@app.get("/authors/{author_id}/", response_model=schemas.Author)
def read_author(db: SessionDep, author_id: int):
    author = crud.get_author_detail(db=db, author_id=author_id)
    if author is None:
        raise HTTPException(status_code=404, detail="Author not found")
    return author


@app.post("/authors/", response_model=schemas.Author)
def create_author(db: SessionDep, author: schemas.AuthorCreate):
    return crud.create_author(db=db, author=author)


@app.get("/books/", response_model=list[schemas.Book])
def read_books(
    db: SessionDep,
    skip: Annotated[int, Query(ge=0)] = 0,
    limit: Annotated[int, Query(ge=1, le=100)] = 10,
    author_ids: Annotated[list[int] | None, Query()] = None,
):
    return crud.get_book_list(db=db, skip=skip, limit=limit, author_ids=author_ids)


@app.post("/books/", response_model=schemas.Book)
def create_book(db: SessionDep, book: schemas.BookCreate):
    return crud.create_book(db=db, book=book)
