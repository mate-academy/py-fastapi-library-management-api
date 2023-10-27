from __future__ import annotations

from sqlalchemy.orm import Session

import models
import schemas


def get_author_list(
    db: Session, skip: int = 0, limit: int = 100
) -> list[models.DBAuthor]:
    return db.query(models.DBAuthor).offset(skip).limit(limit).all()


def get_author_by_name(db: Session, name: str) -> models.DBAuthor | None:
    return db.query(models.DBAuthor).filter(models.DBAuthor.name == name).first()


def get_author(db: Session, author_id: int) -> models.DBAuthor | None:
    return db.query(models.DBAuthor).filter(models.DBAuthor.id == author_id).first()


def create_author(db: Session, author: schemas.AuthorCreate) -> models.DBAuthor:
    db_author = models.DBAuthor(name=author.name, bio=author.bio)
    db.add(db_author)
    db.commit()
    db.refresh(db_author)
    return db_author


def get_book_list(
    db: Session, skip: int = 0, limit: int = 100, author_id: int = None
) -> list[models.DBBook]:
    queryset = db.query(models.DBBook)

    if author_id:
        queryset = queryset.filter(models.DBBook.author_id == author_id)

    return queryset.offset(skip).limit(limit).all()


def create_book(db: Session, book: schemas.BookCreate, author_id: int) -> models.DBBook:
    db_book = models.DBBook(
        title=book.title,
        summary=book.summary,
        publication_date=book.publication_date,
        author_id=author_id,
    )
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book
