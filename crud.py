from datetime import date

from sqlalchemy import select
from sqlalchemy.orm import Session

from db import models
import schemas


def get_all_authors(
    db: Session, limit: int = 10, skip: int = 0, book: str | None = None
):
    queryset = select(models.DBAuthor)

    if book:
        queryset = queryset.where(models.DBAuthor.books.name == book)

    queryset = queryset.offset(skip).limit(limit)

    return queryset


def get_author_by_name(db: Session, name: str):
    return (
        select(models.DBAuthor).where(models.DBAuthor.name == name)
    )


def get_author_by_id(db: Session, author_id: int):
    return (
        select(models.DBAuthor)
        .where(models.DBAuthor.id == author_id)
    )


def create_author(db: Session, author: schemas.AuthorCreate):
    db_author = models.DBAuthor(**author.model_dump())
    db.add(db_author)
    db.commit()
    db.refresh(db_author)
    return db_author


def get_book_list(
    db: Session,
    skip: int = 0,
    limit: int = 10,
    publication_date: date | None = None,
    author: str | None = None,
):
    queryset = select(models.DBBook)

    if author:
        queryset = queryset.where(models.DBBook.author.name == author)

    if publication_date:
        queryset = queryset.where(
            models.DBBook.publication_date == publication_date
        )

    queryset = queryset.offset(skip).limit(limit)

    return queryset


def get_book(db: Session, book_id: int):
    return select(models.DBBook).where(models.DBBook.id == book_id)


def create_book(db: Session, book: schemas.BookCreate):
    db_book = models.DBBook(**book.model_dump())
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book
