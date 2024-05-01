from datetime import date

from sqlalchemy.orm import Session

import schemas
from db import models


def create_author(session: Session,
                  author: schemas.CreateAuthor) -> models.DBAuthor:
    db_author = models.DBAuthor(
        name=author.name,
        bio=author.bio
    )
    session.add(db_author)
    session.commit()
    session.refresh(db_author)
    return db_author


def get_authors_list(session: Session,
                     skip: int = 0,
                     limit: int = 2):      # What proper type annotation here?
    return session.query(models.DBAuthor).offset(skip).limit(limit).all()


def get_author_by_name(session: Session, author_name: str) -> models.DBAuthor:
    return (
        session.query(
            models.DBAuthor
        ).filter(
            models.DBAuthor.name == author_name
        ).first()
    )


def get_author_by_id(session: Session, author_id: int) -> models.DBAuthor:
    return (
        session.query(
            models.DBAuthor
        ).filter(
            models.DBAuthor.id == author_id
        ).first()
    )


def create_book(session: Session,
                book: schemas.CreateBook) -> models.DBBook:
    db_book = models.DBBook(
        title=book.title,
        summary=book.summary,
        publication_date=book.publication_date,
        author_id=book.author_id
    )
    session.add(db_book)
    session.commit()
    session.refresh(db_book)
    return db_book


def get_books_list(session: Session,
                   skip: int = 0,
                   limit: int = 2):    # What proper type annotation here?
    return session.query(models.DBBook).offset(skip).limit(limit).all()


def get_books_by_id(session: Session, book_id: int) -> models.DBBook:
    return (
        session.query(
            models.DBBook
        ).filter(
            models.DBBook.id == book_id
        ).first()
    )


def get_books_by_name(session: Session, book_title: str) -> models.DBBook:
    return (
        session.query(
            models.DBBook
        ).filter(
            models.DBBook.title == book_title
        ).first()
    )


def get_books_by_author_id(session: Session,
                           author_id: int) -> list[models.DBBook]:
    return (
        session.query(
            models.DBBook
        ).filter(
            models.DBBook.author_id == author_id
        ).all()
    )
