from sqlalchemy.orm import Session

from typing import Optional

import models
import schemas


def get_all_authors(db: Session,
                    skip: int = 0,
                    limit: int = 10) -> list[schemas.Author]:
    return db.query(models.DBAuthor).offset(skip).limit(limit).all()


def get_all_books(db: Session,
                  skip: int = 0,
                  limit: int = 10,
                  author: str | None = None) -> list[schemas.Book]:
    queryset = db.query(models.DBBook)

    if author is not None:
        queryset = queryset.filter(models.DBBook.author.has(name=author))

    return queryset.offset(skip).limit(limit).all()


def get_author(db: Session, author_id: int) -> list[schemas.Author]:
    return db.query(models.DBAuthor).filter(
        models.DBAuthor.id == author_id
    ).first()


def get_book(db: Session, book_id: int) -> list[schemas.Book]:
    return db.query(models.DBBook).filter(
        models.DBBook.id == book_id
    ).first()


def get_author_by_name(db: Session,
                       author_name: str) -> Optional[schemas.Author]:
    return db.query(models.DBAuthor).filter(
        models.DBAuthor.name == author_name
    ).first()


def get_books_by_author_id(db: Session,
                           author_id: int,
                           skip: int = 0,
                           limit: int = 10) -> list[schemas.Book]:
    return (
        db.query(models.DBBook)
        .filter(models.DBBook.author_id == author_id)
        .offset(skip)
        .limit(limit)
        .all()
    )


def get_book_by_title_and_author(db: Session,
                                 book_title: str,
                                 author_id: int) -> Optional[schemas.Book]:
    return (
        db.query(models.DBBook)
        .filter(models.DBBook.title == book_title,
                models.DBBook.author_id == author_id)
        .first()
    )


def create_author(db: Session,
                  author: schemas.AuthorCreate) -> models.DBAuthor:
    db_author = models.DBAuthor(**author.model_dump())
    db.add(db_author)
    db.commit()
    db.refresh(db_author)
    return db_author


def create_book(db: Session,
                book: schemas.BookCreate) -> models.DBAuthor:
    db_book = models.DBBook(**book.model_dump())
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book
