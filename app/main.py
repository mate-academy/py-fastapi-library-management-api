from typing import List

from fastapi import FastAPI, status, Depends
from fastapi_pagination import Page, add_pagination, paginate

from sqlalchemy.orm import Session

from app.custom_exceptions.http_exceptions import (
    AuthorNotFoundException,
    BookNotFoundException
)
from app.db.database import SessionLocal
from app import schemas, crud
from app.db.models import DBBook, DBAuthor

app = FastAPI()


def get_db() -> Session:
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()


@app.get("/")
def root() -> dict:
    return {"message": "Hello world"}


@app.get(
    path="/authors/",
    response_model=Page[schemas.Author],
    status_code=status.HTTP_200_OK,
)
def read_authors(db: Session = Depends(get_db)) -> Page[DBAuthor]:
    return paginate(crud.get_all_authors(db=db))


@app.post(
    path="/authors/",
    response_model=schemas.Author,
    status_code=status.HTTP_201_CREATED,
)
def create_author(
        author: schemas.AuthorCreate,
        db: Session = Depends(get_db)
) -> DBAuthor:
    return crud.create_author(
        db=db,
        author=author
    )


@app.get(
    path="/authors/{author_id}/",
    response_model=schemas.Author,
    status_code=status.HTTP_200_OK,
)
def retrieve_author(
        author_id: int,
        db: Session = Depends(get_db)
) -> DBAuthor:
    author = crud.get_author(db=db, author_id=author_id)

    if author is None:
        raise AuthorNotFoundException
    return author


@app.put(
    path="/authors/{author_id}/update/",
    response_model=schemas.Author,
    status_code=status.HTTP_200_OK,
)
def author_update(
        author_id: int,
        author_data: schemas.AuthorCreate,
        db: Session = Depends(get_db)
) -> DBAuthor:
    updated_author = crud.update_author(
        db=db,
        author_id=author_id,
        author_data=author_data
    )

    if updated_author is None:
        raise AuthorNotFoundException

    return updated_author


@app.delete(
    path="/authors/{author_id}/delete/",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_author(
        author_id: int,
        db: Session = Depends(get_db)
) -> None:
    author = crud.delete_author(db=db, author_id=author_id)

    if author is None:
        raise AuthorNotFoundException


@app.get(
    path="/books/",
    response_model=Page[schemas.Book],
    status_code=status.HTTP_200_OK
)
def read_books(
        db: Session = Depends(get_db),
        author_id: int | None = None,
) -> Page[DBBook]:
    return paginate(crud.get_all_books(db=db, author_id=author_id))


@app.post(
    path="/books/",
    response_model=schemas.Book,
    status_code=status.HTTP_201_CREATED,
)
def create_book(
        book: schemas.BookCreate,
        db: Session = Depends(get_db)
) -> DBBook:
    return crud.create_book(
        db=db,
        book=book
    )


@app.get(
    path="/books/{book_id}/",
    response_model=schemas.Book,
    status_code=status.HTTP_200_OK
)
def retrieve_book(
        book_id: int,
        db: Session = Depends(get_db)
) -> DBBook:
    book = crud.get_book(db=db, book_id=book_id)

    if book is None:
        raise BookNotFoundException

    return book


@app.put(
    path="/books/{book_id}/update/",
    response_model=schemas.Book,
    status_code=status.HTTP_200_OK,
)
def book_update(
        book_id: int,
        book_data: schemas.BookCreate,
        db: Session = Depends(get_db)
) -> DBBook:
    updated_book = crud.update_book(
        book_id=book_id,
        book_data=book_data,
        db=db
    )

    if updated_book is None:
        raise BookNotFoundException

    return updated_book


@app.delete(
    path="/books/{book_id}/delete/",
    status_code=status.HTTP_204_NO_CONTENT,
)
def book_update(
        book_id: int,
        db: Session = Depends(get_db)
) -> None:
    book = crud.delete_book(db=db, book_id=book_id)

    if book is None:
        raise BookNotFoundException


add_pagination(app)
