from collections.abc import Sequence

from sqlalchemy import select
from sqlalchemy.orm import Session

import schemas
import models


# Create a new author
def create_author(
    db: Session,
    author: schemas.AuthorCreate
) -> models.DBAuthor:
    db_author = models.DBAuthor(
        name=author.name,
        bio=author.bio,
    )
    db.add(db_author)
    db.commit()
    db.refresh(db_author)

    return db_author


# Retrieve a list of authors with pagination (skip, limit)
def get_all_authors(
    db: Session,
    skip: int = 0,
    limit: int = 10
) -> Sequence[models.DBAuthor]:
    return db.scalars(
        select(models.DBAuthor)
        .order_by(models.DBAuthor.id)
        .offset(skip)
        .limit(limit)
    ).all()


# Retrieve a single author by ID
def get_author_by_id(
    db: Session,
    author_id: int
) -> models.DBAuthor | None:
    return db.scalar(
        select(models.DBAuthor).where(models.DBAuthor.id == author_id)
    )


def get_author_by_name(db: Session, name: str) -> models.DBAuthor | None:
    return db.scalar(
        select(models.DBAuthor).where(models.DBAuthor.name == name)
    )


# Retrieve a list of books with pagination (skip, limit)
# Filter books by author ID
def get_all_books(
    db: Session,
    skip: int = 0,
    limit: int = 10,
    author_id: int | None = None
) -> Sequence[models.DBBook]:
    stmt = select(models.DBBook)

    if author_id is not None:
        stmt = stmt.where(models.DBBook.author_id == author_id)

    return db.scalars(
        stmt
        .order_by(models.DBBook.id)
        .offset(skip)
        .limit(limit)
    ).all()


# Create a new book for a specific author
def create_book(db: Session, book: schemas.BookCreate) -> models.DBBook:
    db_book = models.DBBook(
        author_id=book.author_id,
        title=book.title,
        summary=book.summary,
        publication_date=book.publication_date,
    )
    db.add(db_book)
    db.commit()
    db.refresh(db_book)

    return db_book
