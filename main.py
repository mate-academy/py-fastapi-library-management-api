from typing import Annotated

from fastapi import FastAPI, Depends, status, HTTPException
from sqlalchemy.orm import Session

from models import Base
from schemas import (
    AuthorCreateSchema,
    AuthorReadSchema,
    BookReadSchema,
    BookCreateSchema
)
from crud import (
    get_all_authors,
    create_author,
    get_all_books,
    create_book,
    get_author
)
from database import get_db, engine

Base.metadata.create_all(bind=engine)

app = FastAPI()


@app.get("/authors/", response_model=list[AuthorReadSchema])
def read_authors(
    db: Annotated[Session, Depends(get_db)],
    skip: int = 0,
    limit: int = 10
):
    return get_all_authors(db=db, to_skip=skip, to_limit=limit)


@app.get("/authors/{author_id}/", response_model=AuthorReadSchema)
def read_single_author(
    author_id: int,
    db: Annotated[Session, Depends(get_db)]
):
    author = get_author(db=db, author_id=author_id)

    if author is None:
        raise HTTPException(status_code=404, detail="Author not found")
    return author


@app.post(
    "/authors/",
    response_model=AuthorReadSchema,
    status_code=status.HTTP_201_CREATED
)
def make_author(
    author_data: AuthorCreateSchema,
    db: Annotated[Session, Depends(get_db)]
):
    return create_author(db=db, author_data=author_data)


@app.get("/books/", response_model=list[BookReadSchema])
def read_books(
    db: Annotated[Session, Depends(get_db)],
    author_id: int = None,
    skip: int = 0,
    limit: int = 10
):
    return get_all_books(
        db=db,
        author_id=author_id,
        to_skip=skip,
        to_limit=limit
    )


@app.post(
    "/books/",
    response_model=BookReadSchema,
    status_code=status.HTTP_201_CREATED
)
def make_book(
    book_data: BookCreateSchema,
    db: Annotated[Session, Depends(get_db)]
):
    return create_book(db=db, book_data=book_data)
