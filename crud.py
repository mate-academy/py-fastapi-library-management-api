from typing import Optional

from sqlalchemy.orm import Session

import schemas
import models
from schemas import AuthorCreate


def get_all_authors(db: Session) -> list[schemas.Author]:
    return db.query(models.DBAuthor).all()


def get_author_by_name(db: Session, name: str) -> Optional[models.DBAuthor]:
    return (
        db.query(models.DBAuthor).filter(models.DBAuthor.name == name).first()
    )


def create_author(db: Session, author: AuthorCreate) -> schemas.Author:
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
    author: str | None = None,
) -> Optional[models.DBAuthor]:
    queryset = db.query(models.DBBook)

    if author:
        queryset = queryset.filter(models.DBBook.author.has(name=author))

    return queryset.all()


def get_book(db: Session, book_id: int) -> models.DBBook:
    return db.query(models.DBBook).filter(models.DBBook.id == book_id).first()


def create_book(db: Session, book: schemas.BookCreate) -> models.DBBook:
    db_book = models.DBBook(
        title=book.title,
        summary=book.summary,
        publication_date=book.publication_date,
        author_id=book.author_id
    )
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book
