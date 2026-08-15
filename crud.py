from collections.abc import Sequence

from sqlalchemy import select
from sqlalchemy.orm import Session

import models
import schemas


def get_all_authors(db: Session, skip: int = 0, limit: int = 10) -> Sequence[models.DBAuthor]:
    stmt = select(models.DBAuthor).offset(skip).limit(limit)
    return db.scalars(stmt).all()


def get_author_by_id(db: Session, author_id: int) -> models.DBAuthor | None:
    return db.get(models.DBAuthor, author_id)


def create_author(db: Session, author: schemas.AuthorCreate) -> models.DBAuthor:
    db_author = models.DBAuthor(
        name=author.name,
        bio=author.bio,
    )
    db.add(db_author)
    db.commit()
    db.refresh(db_author)
    return db_author


def get_all_books(
    db: Session,
    skip: int = 0,
    limit: int = 10,
    author_id: int | None = None,
) -> Sequence[models.DBBook]:
    stmt = select(models.DBBook)
    if author_id is not None:
        stmt = stmt.where(models.DBBook.author_id == author_id)
    stmt = stmt.offset(skip).limit(limit)
    return db.scalars(stmt).all()


def create_book(db: Session, book: schemas.BookCreate) -> models.DBBook:
    db_book = models.DBBook(
        title=book.title,
        summary=book.summary,
        publication_date=book.publication_date,
        author_id=book.author_id,
    )
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book