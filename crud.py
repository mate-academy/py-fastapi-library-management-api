from sqlalchemy import select
from sqlalchemy.orm import Session
from typing import List, Optional

import models
import schemas


def get_all_authors(
        db: Session,
        skip: int = 0,
        limit: int = 10,
):
    return db.scalars(select(models.Author)).all()

def create_author(db: Session, author: schemas.CreateAuthor):
    db_author = models.Author(name=author.name, bio=author.bio)
    db.add(db_author)
    db.commit()
    db.refresh(db_author)
    return db_author

def get_author_id(db: Session, author_id: int):
    return db.scalar(
        select(models.Author).where(models.Author.id == author_id)
    )

def create_book(db: Session, book: schemas.CreateBook) -> models.Book:
    book_data = book.model_dump()

    db_book = models.Book(**book_data)

    db.add(db_book)
    db.commit()
    db.refresh(db_book)

    return db_book

def get_books(
        db: Session,
        skip: int = 0,
        limit: int = 10,
        author_id: Optional[int] = None
) -> List[models.Book]:
    stmt = select(models.Book)

    if author_id is not None:
        stmt = stmt.where(models.Book.author_id == author_id)

    stmt = stmt.offset(skip).limit(limit)
    return list(db.scalars(stmt).all())
