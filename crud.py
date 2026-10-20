from sqlalchemy import select
from sqlalchemy.orm import Session

import models
import schemas


def create_author(
    db: Session,
    author: schemas.AuthorCreate,
) -> models.Author:
    db_author = models.Author(**author.model_dump())
    db.add(db_author)
    db.commit()
    db.refresh(db_author)
    return db_author


def get_authors(
    db: Session,
    skip: int = 0,
    limit: int = 100,
) -> list[models.Author]:
    statement = select(models.Author).offset(skip).limit(limit)
    return list(db.scalars(statement).all())


def get_author(
    db: Session,
    author_id: int,
) -> models.Author | None:
    return db.get(models.Author, author_id)


def get_author_by_name(
    db: Session,
    name: str,
) -> models.Author | None:
    statement = select(models.Author).where(
        models.Author.name == name
    )
    return db.scalar(statement)


def create_book(
    db: Session,
    book: schemas.BookCreate,
    author_id: int,
) -> models.Book:
    db_book = models.Book(
        **book.model_dump(),
        author_id=author_id,
    )
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book


def get_books(
    db: Session,
    skip: int = 0,
    limit: int = 100,
    author_id: int | None = None,
) -> list[models.Book]:
    statement = select(models.Book)

    if author_id is not None:
        statement = statement.where(
            models.Book.author_id == author_id
        )

    statement = statement.offset(skip).limit(limit)
    return list(db.scalars(statement).all())
