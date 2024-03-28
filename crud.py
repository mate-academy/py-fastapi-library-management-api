from typing import Optional

from sqlalchemy.orm import Session

import models
from schemas import AuthorCreate, BookCreate


def get_all_authors(
        db: Session,
        skip: int | None = None,
        limit: int | None = None
) -> Optional[models.DBAuthor]:
    return db.query(models.DBAuthor).offset(skip).limit(limit).all()


def get_author_by_name(db: Session, name: str) -> Optional[models.DBAuthor]:
    return db.query(models.DBAuthor).filter(models.DBAuthor.name == name).first()


def get_author(db: Session, author_id: int) -> Optional[models.DBAuthor]:
    return db.query(models.DBAuthor).filter(models.DBAuthor.id == author_id).first()


def create_author(db: Session, author: AuthorCreate) -> Optional[models.DBAuthor]:
    db_author = models.DBAuthor(
        name=author.name,
        bio=author.bio
    )
    db.add(db_author)
    db.commit()
    db.refresh(db_author)
    return db_author


def get_all_books(
        db: Session,
        author_id: int | None = None,
        skip: int | None = None,
        limit: int | None = None
) -> Optional[models.DBBook]:
    queryset = db.query(models.DBBook)

    if author_id is not None:
        queryset = queryset.filter(models.DBBook.author.has(id=author_id))

    return queryset.all().offset(skip).limit(limit).all()


def create_book(db: Session, book: BookCreate) -> Optional[models.DBBook]:
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


def get_book_by_title(db: Session, title: str) -> Optional[models.DBBook]:
    return db.query(models.DBBook).filter(models.DBBook.title == title).first()
