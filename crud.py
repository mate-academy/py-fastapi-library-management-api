from typing import List, Optional
from sqlalchemy.orm import Session

from db import models
import schemas


def get_all_authors(
    db: Session, skip: int = 0, limit: int = 10
) -> List[models.DBAuthor]:
    return db.query(models.DBAuthor).offset(skip).limit(limit).all()


def get_author_by_name(db: Session, name: str) -> Optional[models.DBAuthor]:
    return db.query(models.DBAuthor).filter(models.DBAuthor.name == name).first()


def get_author_by_id(db: Session, author_id: int) -> Optional[models.DBAuthor]:
    return db.query(models.DBAuthor).filter(models.DBAuthor.id == author_id).first()


def create_author(db: Session, author: schemas.AuthorCreate) -> models.DBAuthor:
    db_author = models.DBAuthor(name=author.name, bio=author.bio)
    db.add(db_author)
    db.commit()
    db.refresh(db_author)
    return db_author


def get_all_books(db: Session, skip: int = 0, limit: int = 10) -> List[models.DBBook]:
    return db.query(models.DBBook).offset(skip).limit(limit).all()


def get_book_by_author_id(
    db: Session, author_id: int | None = None, skip: int = 0, limit: int = 10
) -> List[models.DBBook]:
    queryset = db.query(models.DBBook)

    if author_id is not None:
        queryset = queryset.filter(models.DBBook.author_id == author_id)

    return queryset.offset(skip).limit(limit).all()


def create_book(db: Session, book: schemas.BookCreate) -> models.DBBook:
    db_book = models.DBBook(
        title=book.title,
        summary=book.summary,
        publication=book.publication,
        author_id=book.author_id,
    )
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book
