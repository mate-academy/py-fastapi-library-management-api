from sqlalchemy import select
from sqlalchemy.orm import Session

import models
import schemas


def get_authors(db: Session, skip: int = 0, limit: int = 100) -> list[models.Author]:
    stmt = select(models.Author).order_by(models.Author.name).offset(skip).limit(limit)
    return list(db.scalars(stmt).all())


def get_author(db: Session, author_id: int) -> models.Author | None:
    return db.get(models.Author, author_id)


def get_author_by_name(db: Session, name: str) -> models.Author | None:
    stmt = select(models.Author).where(models.Author.name == name)
    return db.scalars(stmt).first()


def create_author(db: Session, author: schemas.AuthorCreate) -> models.Author:
    db_author = models.Author(**author.model_dump())
    db.add(db_author)
    db.commit()
    db.refresh(db_author)
    return db_author


def get_books(
    db: Session,
    skip: int = 0,
    limit: int = 100,
    author_id: int | None = None,
) -> list[models.Book]:
    stmt = select(models.Book)
    if author_id is not None:
        stmt = stmt.where(models.Book.author_id == author_id)
    stmt = stmt.order_by(models.Book.title, models.Book.id).offset(skip).limit(limit)
    return list(db.scalars(stmt).all())


def get_book(db: Session, book_id: int) -> models.Book | None:
    return db.scalars(select(models.Book).where(models.Book.id == book_id)).first()


def get_book_by_name(db: Session, name: str) -> models.Book | None:
    return db.scalars(select(models.Book).where(models.Book.title == name)).first()


def create_book(db: Session, book: schemas.BookCreate, author_id: int) -> models.Book:
    db_book = models.Book(**book.model_dump(), author_id=author_id)
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book
