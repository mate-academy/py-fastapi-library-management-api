from typing import List, Union

from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session

import crud
import schemas
from database import SessionLocal
from models import Author, Book


def get_db() -> Session:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def validate_author_uniqueness(
    author: schemas.AuthorCreate, db: Session = Depends(get_db)
) -> None:
    existing_author = crud.get_author_by_name(db=db, author_name=author.name)

    if existing_author:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"Author with the name: '{author.name}' already exists.",
        )


def validate_book_uniqueness(
    book: schemas.BookCreate, db: Session = Depends(get_db)
) -> None:
    existing_book = crud.get_book_by_title(db=db, book_title=book.title)

    if existing_book:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"Book with the title: '{book.title}' already exists.",
        )


def validate_author_id(
    author_id: int, db: Session = Depends(get_db)
) -> Union[Author, None]:
    author = crud.get_author_by_id(db=db, author_id=author_id)

    if not author:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Author with id {author_id} not found",
        )

    return author


def fetch_books_with_optional_filter(
    skip: int = 0,
    limit: int = 5,
    author_id: int | None = None,
    db: Session = Depends(get_db),
) -> List[Book]:
    if not author_id:
        return crud.get_book_list(db=db, skip=skip, limit=limit)

    return crud.filter_book_by_author_id(db=db, author_id=author_id)
