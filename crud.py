from typing import Any, Sequence

from sqlalchemy import select
from sqlalchemy.orm import Session

import models
import schemas


def get_all_authors(
        db: Session, skip: int = 0, limit: int = 10
) -> Sequence[models.Author]:

    return db.scalars(
        select(models.Author)
        .offset(skip)
        .limit(limit)
    ).all()


def create_author(
        db: Session, author_in: schemas.AuthorCreate
) -> models.Author:
    db_author = models.Author(**author_in.model_dump())
    db.add(db_author)
    db.commit()
    db.refresh(db_author)

    return db_author


def get_author_by_id(db: Session, author_id: int) -> models.Author | None:
    return db.scalar(
        select(models.Author)
        .where(models.Author.id == author_id)
    )


def create_book(
        db: Session,
        book_in: schemas.BookCreate,
        author_id: int
) -> models.Book | None:
    db_book = models.Book(
        **book_in.model_dump(),
        author_id=author_id
    )
    db.add(db_book)
    db.commit()
    db.refresh(db_book)

    return db_book


def get_all_books(
        db: Session,
        skip: int = 0,
        limit: int = 10
) -> Sequence[models.Book]:

    return db.scalars(
        select(models.Book)
        .offset(skip)
        .limit(limit)
    ).all()


def get_books_by_author(
        db: Session,
        author_id: int,
        skip: int = 0,
        limit: int = 10
) -> Sequence[models.Book]:

    return db.scalars(
        select(models.Book)
        .where(models.Book.author_id == author_id)
        .offset(skip)
        .limit(limit)
    ).all()
