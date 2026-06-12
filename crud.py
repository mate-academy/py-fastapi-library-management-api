from sqlalchemy import select
from sqlalchemy.orm import Session

import schemas
import models


def get_all_authors(db: Session) -> list[models.Author]:
    return db.scalars(select(models.Author)).all()


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
    authors: str | None = None,
) -> list[models.Book]:
    stmt = select(models.Book)

    if authors:
        stmt = stmt.join(models.Author).where(models.Author.name == authors)

    return db.scalars(stmt).all()


def get_book_by_id(db: Session, book_id: int) -> models.Book | None:
    return db.scalar(select(models.Book).where(models.Book.id == book_id))


def get_book_by_title(db: Session, title: str) -> models.Book | None:
    return db.scalar(select(models.Book).where(models.Book.title == title))


def create_book(db: Session, book: schemas.BookCreate) -> models.Book:
    db_book = models.Book(
        author_id=book.author_id,
        title=book.title,
        price=book.price,
        packaging_type=book.packaging_type,
    )
    db.add(db_book)
    db.commit()
    db.refresh(db_book)

    return db_book