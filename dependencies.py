from typing import List, Union

from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session

import crud
from database import SessionLocal
from models import Author, Book


def get_db() -> Session:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


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
