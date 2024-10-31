from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Optional, List

import schemas
from crud import (
    get_all_authors,
    create_author as crud_create_author,
    get_author_detail,
    get_all_books,
    create_book as crud_create_book,
)
from database import get_db
from settings import API_PREFIX

app = FastAPI()


def raise_not_found_exception(instance, id: int):
    if instance is None:
        raise HTTPException(
            status_code=404,
            detail=f"Item with id {id} not found!"
        )


@app.get(API_PREFIX + "authors/", response_model=List[schemas.Author])
def read_all_authors(
        skip: Optional[int] = None,
        limit: Optional[int] = None,
        db: Session = Depends(get_db)
) -> List[schemas.Author]:
    return get_all_authors(db=db, skip=skip, limit=limit)


@app.post(API_PREFIX + "authors/", response_model=schemas.Author)
def create_author_route(
        author: schemas.AuthorCreate,
        db: Session = Depends(get_db)
) -> schemas.Author:
    return crud_create_author(db=db, author=author)


@app.get(API_PREFIX + "authors/{id}/", response_model=schemas.Author)
def read_author(
        id: int,
        db: Session = Depends(get_db)
) -> schemas.Author:
    author = get_author_detail(db=db, id=id)
    raise_not_found_exception(author, id)
    return author


@app.get(API_PREFIX + "books/", response_model=List[schemas.Book])
def read_all_books(
        skip: Optional[int] = None,
        limit: Optional[int] = None,
        author_id: Optional[int] = None,
        db: Session = Depends(get_db)
) -> List[schemas.Book]:
    return get_all_books(db=db, skip=skip, limit=limit, author_id=author_id)


@app.post(API_PREFIX + "books/", response_model=schemas.Book)
def create_book_route(
        book: schemas.BookCreate,
        db: Session = Depends(get_db)
) -> schemas.Book:
    return crud_create_book(db=db, book=book)
