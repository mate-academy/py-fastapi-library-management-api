from typing import List, Annotated, Any

from fastapi import FastAPI, HTTPException
from fastapi.params import Depends, Query
from sqlalchemy.orm import Session

import crud
import schemas
from crud import AlreadyExists, IncorrectFK
from database import get_session

app = FastAPI()


@app.get("/authors/", response_model=List[schemas.AuthorRead])
def read_authors(
    skip: Annotated[int, Query(ge=0)] = 0,
    limit: Annotated[int, Query(ge=1, le=100)] = 100,
    db: Session = Depends(get_session),
) -> List[schemas.AuthorRead]:
    return crud.get_authors_list(db, skip, limit)


@app.get("/authors/{author_id}/", response_model=schemas.AuthorRead)
def read_one_author(author_id: int, db: Session = Depends(get_session)) -> Any:
    author = crud.get_author_by_id(db, author_id)
    if not author:
        raise HTTPException(status_code=404, detail="Author not found")
    return author


@app.post("/authors/", response_model=schemas.AuthorRead)
def create_author(
    data: schemas.AuthorCreate, db: Session = Depends(get_session)
) -> Any:
    try:
        author = crud.create_author(db, data)
    except AlreadyExists:
        raise HTTPException(
            status_code=409, detail="Author with that name already exists"
        )
    return author


@app.get("/books/", response_model=List[schemas.BookRead])
def read_books(
    skip: Annotated[int, Query(ge=0)] = 0,
    limit: Annotated[int, Query(ge=1, le=100)] = 100,
    author_id: Annotated[int | None, Query(ge=1)] = None,
    db: Session = Depends(get_session),
) -> List[schemas.BookRead]:
    return crud.get_books_list(db, author_id, skip, limit)


@app.get("/books/{book_id}", response_model=schemas.BookRead)
def read_one_book(book_id: int, db: Session = Depends(get_session)) -> Any:
    book = crud.get_book_by_id(db, book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return book


@app.post("/books/", response_model=schemas.BookRead)
def create_book(
    data: schemas.BookCreate, db: Session = Depends(get_session)
) -> Any:
    try:
        book = crud.create_book(db, data)
    except IncorrectFK:
        raise HTTPException(
            status_code=404, detail="Author with that id is not found"
        )
    return book
