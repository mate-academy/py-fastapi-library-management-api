from sqlalchemy import select
from sqlalchemy.orm import Session

import schemas
import models


def get_authors_list(
        db: Session,
        skip: int = 0,
        limit: int = 10
) -> list[models.DBAuthor]:
    return db.scalars(select(models.DBAuthor).offset(skip).limit(limit)).all()


def get_author_by_id(db: Session, author_id: int) -> models.DBAuthor | None:
    return db.scalar(select(models.DBAuthor).where(models.DBAuthor.id == author_id))


def create_author(db: Session, author: schemas.AuthorCreate) -> models.DBAuthor:
    db_author = models.DBAuthor(
        name=author.name,
        bio=author.bio,
    )
    db.add(db_author)
    db.commit()
    db.refresh(db_author)
    return db_author


def get_author_by_name(db: Session, name: str) -> models.DBAuthor | None:
    return db.scalar(select(models.DBAuthor).where(models.DBAuthor.name == name))


def get_books_list(
        db: Session,
        skip: int = 0,
        limit: int = 10,
        author_id: int | None = None,
) -> list[models.DBBook]:
    queryset = select(models.DBBook)

    if author_id is not None:
        queryset = queryset.join(models.DBAuthor).where(models.DBAuthor.id == author_id)

    queryset = queryset.offset(skip).limit(limit)
    return db.scalars(queryset).all()


def get_book_by_id(db: Session, book_id: int) -> models.DBBook | None:
    return db.scalar(select(models.DBBook).where(models.DBBook.id == book_id))


def get_book_by_title(db: Session, title: str) -> models.DBBook | None:
    return db.scalar(select(models.DBBook).where(models.DBBook.title == title))


def create_book(db: Session, book: schemas.BookCreate) -> models.DBBook:
    de_book = models.DBBook(
        author_id=book.author_id,
        title=book.title,
        summary=book.summary,
        publication_date=book.publication_date,
    )
    db.add(de_book)
    db.commit()
    db.refresh(de_book)
    return de_book
