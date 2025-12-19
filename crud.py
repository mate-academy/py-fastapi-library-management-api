from typing import Optional

import models
import schemas
from sqlalchemy.orm import Session
from sqlalchemy import select


def get_authors(db: Session, skip: int = 0, limit: int = 2):
    return db.query(models.Author).offset(skip).limit(limit).all()


def get_author(db: Session, author_id: int):
    stmt = select(models.Author).where(models.Author.id == author_id)
    return db.scalar(stmt)


def create_author(db: Session, author: schemas.AuthorCreate):
    author_to_add = models.Author(**author.model_dump())
    try:
        db.add(author_to_add)
        db.commit()
        db.refresh(author_to_add)
        return author_to_add
    except:
        db.rollback()
        raise


def create_book(db: Session, book: schemas.BookCreate):
    book_to_add = models.Book(**book.model_dump())
    try:
        db.add(book_to_add)
        db.commit()
        db.refresh(book_to_add)
        return book_to_add
    except:
        db.rollback()
        raise


def get_books(
    db: Session,
    skip: int = 0,
    limit: int = 2,
    author_id: Optional[int] = None,
):
    stmt  = select(models.Book)

    if author_id is not None:
        stmt = stmt.where(models.Author.id == author_id)

    return db.scalars(stmt.offset(skip).limit(limit)).all()

