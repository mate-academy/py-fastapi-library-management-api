from sqlalchemy.orm import Session
from typing import Optional

from db import models
import schemas


def get_all_authors(db: Session) -> list[models.Author]:
    return db.query(models.Author).all()


def get_author_by_id(db: Session, author_id: int) -> Optional[models.Author]:
    return db.query(models.Author).filter(models.Author.id == author_id).first()


def get_author_by_name(db: Session, name: str) -> Optional[models.Author]:
    return (
        db.query(models.Author).filter(models.Author.name == name).first()
    )


def create_author(db: Session, author: schemas.AuthorCreate) -> Optional[models.Author]:
    db_author = models.Author(
        name=author.name,
        bio=author.bio
    )

    db.add(db_author)
    db.commit()
    db.refresh(db_author)

    return db_author


def get_books_list(
        db: Session,
        author_id: int | None = None
) -> Optional[models.Book] | list[models.Book]:
    queryset = db.query(models.Book)

    if author_id is not None:
        queryset.filter(models.Book.author_id == author_id)

    return queryset.all()


def get_book_by_id(db: Session, book_id: int) -> Optional[models.Book]:
    return db.query(models.Book).filter(models.Book.id == book_id).first()


def create_book(db: Session, book: schemas.BookCreate) -> Optional[models.Book]:
    db_book = models.Book(
        title=book.title,
        summary=book.summary,
        publication_date=book.publication_date,
        author_id=book.author_id
    )

    db.add(db_book)
    db.commit()
    db.refresh(db_book)

    return db_book
