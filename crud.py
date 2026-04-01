from collections.abc import Sequence

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session, selectinload

import models
import schemas


class AuthorAlreadyExists(Exception):
    """Raised when attempting to create an author with a duplicate name."""

    pass


class AuthorNotFound(Exception):
    """Raised when the specified author ID does not exist."""

    pass


def create_author(db: Session, author: schemas.AuthorCreate) -> models.Author:
    try:
        db_author = models.Author(**author.model_dump())
        db.add(db_author)
        db.commit()
        db.refresh(db_author)
    except IntegrityError:
        db.rollback()
        raise AuthorAlreadyExists()
    return db_author


def get_author(db: Session, author_id: int) -> models.Author | None:
    return db.scalar(
        select(models.Author)
        .options(selectinload(models.Author.books))
        .where(models.Author.id == author_id)
    )


def get_authors(db: Session, skip: int = 0, limit: int = 10) -> Sequence[models.Author]:
    return db.scalars(select(models.Author).offset(skip).limit(limit)).all()


def create_book(db: Session, book: schemas.BookCreate) -> models.Book:
    author = db.scalar(select(models.Author).where(models.Author.id == book.author_id))
    if author is None:
        raise AuthorNotFound()

    db_book = models.Book(**book.model_dump())
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book


def get_books(
    db: Session,
    skip: int = 0,
    limit: int = 10,
    author_id: int | None = None,
) -> Sequence[models.Book]:
    query = select(models.Book)

    if author_id is not None:
        query = query.where(models.Book.author_id == author_id)

    return db.scalars(query.offset(skip).limit(limit)).all()
