from sqlalchemy import select
from sqlalchemy.orm import Session

import schemas
import models


def get_authors(db: Session, skip: int = 0, limit: int = 10) -> list[models.Author]:
    stmt = select(models.Author).order_by(models.Author.id).offset(skip).limit(limit)
    return list(db.scalars(stmt).all())


def get_author(db: Session, author_id: int) -> models.Author | None:
    return db.get(models.Author, author_id)


def get_author_by_name(db: Session, name: str) -> models.Author | None:
    return db.scalar(select(models.Author).where(models.Author.name == name))


def create_author(db: Session, data: schemas.AuthorCreate) -> models.Author:
    author = models.Author(**data.model_dump())
    db.add(author)
    db.commit()
    db.refresh(author)
    return author


def get_books(
    db: Session, author_id: int | None = None, skip: int = 0, limit: int = 10
) -> list[models.Book]:
    stmt = select(models.Book).order_by(models.Book.id)
    if author_id is not None:
        stmt = stmt.where(models.Book.author_id == author_id)
    stmt = stmt.offset(skip).limit(limit)
    return list(db.scalars(stmt).all())


def get_book(db: Session, book_id: int) -> models.Book | None:
    return db.get(models.Book, book_id)


def create_book(db: Session, data: schemas.BookCreate) -> models.Book | None:
    author = db.get(models.Author, data.author_id)
    if author is None:
        return None

    book = models.Book(**data.model_dump())
    db.add(book)
    db.commit()
    db.refresh(book)
    return book
