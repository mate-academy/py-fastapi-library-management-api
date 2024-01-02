from fastapi import Depends, FastAPI, Query, status
from sqlalchemy.orm import Session

import crud
import schemas
from dependencies import (fetch_books_with_optional_filter,
                          get_db,
                          validate_author_id)


app = FastAPI()


@app.get("/")
def index():
    return {"detail": "library management api"}


@app.get("/authors/", response_model=list[schemas.Author])
def read_author_list(
    db: Session = Depends(get_db),
    skip: int = Query(0, ge=0),
    limit: int = Query(5)
):
    return crud.get_author_list(db=db, skip=skip, limit=limit)


@app.get("/authors/{author_id}/", response_model=schemas.Author)
def read_author(author=Depends(validate_author_id)):
    return author


@app.post(
    "/authors/",
    response_model=schemas.Author,
    status_code=status.HTTP_201_CREATED,
    responses={
        422: {
            "model": schemas.ValidationErrorResponse,
            "description": "Validation Error",
        }
    },
)
def create_author(
    author: schemas.AuthorCreate,
    db: Session = Depends(get_db),
):
    return crud.create_author(db=db, author=author)


@app.get("/books/", response_model=list[schemas.BookBase])
def read_book_list(
    book_list: Session = Depends(fetch_books_with_optional_filter)
):
    return book_list


@app.post(
    "/books/",
    response_model=schemas.BookCreate,
    status_code=status.HTTP_201_CREATED,
    responses={
        422: {
            "model": schemas.ValidationErrorResponse,
            "description": "Validation Error",
        }
    },
)
def create_book(
    book: schemas.BookCreate,
    db: Session = Depends(get_db),
):
    return crud.create_book(db=db, book=book)
