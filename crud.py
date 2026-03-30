from datetime import date

from sqlalchemy import select
from sqlalchemy.orm import Session

import schemas
from db import models


def get_all_authors(
    db: Session, skip: int = 0, limit: int = 10
) -> list[models.DBAuthor]:
    stmt = select(models.DBAuthor).offset(skip).limit(limit)
    return db.scalars(stmt).all()


def get_author_by_id(db: Session, author_id: int) -> models.DBAuthor | None:
    return db.scalar(select(models.DBAuthor).where(models.DBAuthor.id == author_id))


def create_author(db: Session, author: schemas.AuthorCreate) -> models.DBAuthor:
    db_author = models.DBAuthor(
        name=author.name,
        bio=author.bio,
    )
    db.add(db_author)
    db.commit()
    db.refresh(db_author)

    return db_author


def get_author_by_name(db: Session, name: str) -> models.DBAuthor | None:
    return db.scalar(select(models.DBAuthor).where(models.DBAuthor.name == name))


def get_all_books(
    db: Session, author_id: int | None = None, skip: int = 0, limit: int = 10
) -> list[models.DBBook]:
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


def get_book_by_id(db: Session, book_id: int) -> models.DBBook | None:
    return db.scalar(select(models.DBBook).where(models.DBBook.id == book_id))


def get_book_by_title(db: Session, title: str) -> models.DBBook | None:
    return db.scalar(select(models.DBBook).where(models.DBBook.title == title)).first()
