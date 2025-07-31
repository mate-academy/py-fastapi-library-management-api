from typing import Iterator

from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

from crud import (
    get_all_authors_with_pagination,
    get_author_by_id, create_author,
    get_books_by_author_id,
    get_all_books_with_pagination,
    get_book_by_id,
    create_book, get_author_by_name,
    get_book_by_title
)
from schemas import (
    AuthorSchema,
    AuthorCreateSchema,
    BookSchema,
    BookCreateSchema
)
from db.database import SessionLocal
from db.models import Author


app = FastAPI()


def get_db() -> Iterator[Session]:
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()


def get_existing_author(
        author_id: int,
        db: Session = Depends(get_db)
) -> Author:
    author = get_author_by_id(db, author_id)
    if not author:
        raise HTTPException(status_code=404, detail="Author is not found")
    return author


@app.get("/")
def root() -> dict:
    return {"message": "Welcome to Library"}


@app.get("/authors/", response_model=list[AuthorSchema])
def read_all_authors(
        skip: int = 0,
        limit: int = 10,
        db: Session = Depends(get_db)
):
    return get_all_authors_with_pagination(db, skip=skip, limit=limit)


@app.get("/authors/{author_id}/", response_model=AuthorSchema)
def read_author_by_id(author: Author = Depends(get_existing_author)):
    return author


@app.post("/authors/", response_model=AuthorSchema)
def create_new_author(
        author: AuthorCreateSchema,
        db: Session = Depends(get_db)
):
    new_author = get_author_by_name(db=db, name=author.name)
    if new_author:
        raise HTTPException(
            status_code=400,
            detail="Such author already exists"
        )
    return create_author(db, author)


@app.get("/authors/{author_id}/books/", response_model=list[BookSchema])
def read_books_by_author_id(
        author: Author = Depends(get_existing_author),
        skip: int = 0,
        limit: int = 10,
        db: Session = Depends(get_db)
):
    return get_books_by_author_id(db, author.id, skip=skip, limit=limit)


@app.get("/books/", response_model=list[BookSchema])
def read_all_books(
        skip: int = 0,
        limit: int = 10,
        db: Session = Depends(get_db)
):
    return get_all_books_with_pagination(db, skip=skip, limit=limit)


@app.get("/books/{book_id}/", response_model=BookSchema)
def read_book_by_id(
        book_id: int,
        db: Session = Depends(get_db)
):
    book = get_book_by_id(db, book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Book is not found")
    return book


@app.post("/books/", response_model=BookSchema)
def create_new_book(
        book: BookCreateSchema,
        db: Session = Depends(get_db)
):
    author = get_author_by_id(db, book.author_id)
    if not author:
        raise HTTPException(
            status_code=404,
            detail="Author for book is not found"
        )
    new_book = get_book_by_title(db=db, title=book.title)
    if new_book:
        raise HTTPException(
            status_code=400,
            detail="Book with such title already exists"
        )
    return create_book(db, book)
