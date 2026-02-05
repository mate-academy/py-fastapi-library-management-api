import datetime

from sqlalchemy import select
from sqlalchemy.orm import Session

import models
import schemas


def get_authors(db: Session, skip: int = 0, limit: int = 100):
    queryset = select(models.Author).offset(skip).limit(limit)
    return db.scalars(queryset).all()


def get_author_by_id(db: Session, author_id: int):
    return db.scalar(select(models.Author).where(models.Author.id == author_id))


def get_author_by_name(db: Session, name: str):
    return db.scalar(select(models.Author).where(models.Author.name == name))


def create_author(db: Session, author: schemas.AuthorCreate):
    db_author = models.Author(
        name=author.name,
        bio=author.bio
    )
    db.add(db_author)
    db.commit()
    db.refresh(db_author)

    return db_author


def get_books(
        db: Session,
        skip: int = 0,
        limit: int = 100,
        author_id: int | None = None,
        publication_date: datetime.date | None = None,
):
    queryset = select(models.Book)
    if author_id is not None:
        queryset = queryset.where(models.Book.author_id == author_id)
    if publication_date is not None:
        queryset = queryset.where(models.Book.publication_date == publication_date)
    queryset = queryset.offset(skip).limit(limit)
    return db.scalars(queryset).all()


def get_book(db: Session, book_id: int):
    return db.scalar(select(models.Book).where(models.Book.id == book_id))


def create_book_for_author(
        db: Session,
        author_id: int,
        book: schemas.BookCreate
):
    db_book = models.Book(
        title=book.title,
        summary=book.summary,
        publication_date=book.publication_date,
        author_id=author_id
    )
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book
