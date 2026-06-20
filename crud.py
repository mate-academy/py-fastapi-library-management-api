from sqlalchemy import select
from sqlalchemy.orm import Session

import schemas
import models


def get_all_authors(
        db: Session,
        skip: int,
        limit: int
) -> list[models.Author]:
    stmt = select(models.Author)
    if skip:
        stmt = stmt.offset(skip)
    if limit:
        stmt = stmt.limit(limit)
    return db.scalars(stmt).all()


def get_author_by_id(
    db: Session, author_id: int
) -> models.Author | None:
    return db.scalar(
        select(models.Author).where(models.Author.id == author_id)
    )


def create_author(
    db: Session,
    author: schemas.AuthorCreate
) -> models.Author:
    db_author = models.Author(
        name=author.name,
        bio=author.bio,
    )
    db.add(db_author)
    db.commit()
    db.refresh(db_author)

    return db_author


def get_author_by_name(db: Session, name: str) -> models.Author | None:
    return db.scalar(
        select(models.Author).where(models.Author.name == name)
    )


def get_book_list(
    db: Session,
    skip: int,
    limit: int,
    author_id: int | None = None,
) -> list[models.Book]:
    stmt = select(models.Book)

    if skip:
        stmt = stmt.offset(skip)

    if limit:
        stmt = stmt.limit(limit)

    if author_id:
        stmt = stmt.where(models.Book.author_id == author_id)

    return db.scalars(stmt).all()


def get_book_by_id(db: Session, book_id: int) -> models.Book | None:
    return db.scalar(select(models.Book).where(models.Book.id == book_id))


def create_book(db: Session, book: schemas.BookCreate) -> models.Book:
    db_book = models.Book(
        author_id=book.author_id,
        title=book.title,
        summary=book.summary,
        publication_date=book.publication_date,
    )
    db.add(db_book)
    db.commit()
    db.refresh(db_book)

    return db_book
