from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

import schemas
from crud import (
    get_all_authors,
    create_author,
    get_author_detail,
    get_all_books,
    create_book,
)
from database import get_db
from settings import API_PREFIX


app = FastAPI()


@app.get(API_PREFIX + "authors/", response_model=list[schemas.Author])
def read_all_authors(
        skip: int | None = None,
        limit: int | None = None,
        db: Session = Depends(get_db)
) -> list[schemas.Author]:
    return get_all_authors(db=db, skip=skip, limit=limit)


@app.post(API_PREFIX + "authors/", response_model=schemas.Author)
def create_author(
        author: schemas.AuthorCreate,
        db: Session = Depends(get_db)
) -> schemas.Author:
    return create_author(db=db, author=author)


@app.get(API_PREFIX + "authors/{id}/", response_model=schemas.Author)
def read_author(
        id: int,
        db: Session = Depends(get_db)
) -> schemas.Author:
    author = get_author_detail(db=db, id=id)

    if author is None:
        raise HTTPException(
            status_code=404,
            detail=f"Author with id {id} not found!"
        )

    return author


@app.get(API_PREFIX + "books/", response_model=list[schemas.Book])
def read_all_books(
        skip: int | None = None,
        limit: int | None = None,
        author_id: int | None = None,
        db: Session = Depends(get_db)
) -> list[schemas.Book]:
    return get_all_books(db=db, skip=skip, limit=limit, author_id=author_id)


@app.post(API_PREFIX + "books/", response_model=schemas.Book)
def create_book(
        book: schemas.BookCreate,
        db: Session = Depends(get_db)
) -> schemas.Book:
    return create_book(db=db, book=book)
