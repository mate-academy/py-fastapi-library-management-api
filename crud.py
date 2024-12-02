from datetime import date

from sqlalchemy.orm import Session

import schemas
from db import models


def get_all_authors(db: Session):
    return db.query(models.DBAuthor).all()


def get_author_name(db: Session, name: str):
    return (
        db.query(models.DBAuthor)
        .filter(models.DBAuthor.name == name)
        .first()
    )


def create_author(db: Session, author: schemas.AuthorCreate):
    db_author = models.DBAuthor(
        name=author.name,
        bio=author.bio,
    )
    db.add(db_author)
    db.commit()
    db.refresh(db_author)
    return db_author


def get_book_list(
        db: Session,
        title: str | None = None,
        publication_date: date | None = None,
        summary: str | None = None,
        author: str | None = None,
):
    queryset = db.query(models.DBBook)

    if summary is not None:
        queryset = queryset.filter(models.DBBook.summary == summary)

    if title is not None:
        queryset = queryset.filter(models.DBBook.title == title)

    if publication_date is not None:
        queryset = queryset.filter(models.DBBook.publication_date == publication_date)

    if author is not None:
        queryset = queryset.filter(models.DBBook.author.has(name=author))
    return queryset.all()


def get_book(db: Session, book_id: int):
    return db.query(models.DBBook).filter(models.DBBook.id == book_id).first()


def create_book(db: Session, book: schemas.BookCreate):
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

