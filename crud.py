from typing import Sequence

from sqlmodel import Session, select

import models
import shemas
from models import DBBook, DBAuthor


def get_books(db: Session, limit: int, page: int) -> Sequence[DBBook]:
    statement = select(models.DBBook).limit(limit).offset((page - 1) * limit)
    return db.exec(statement).all()


def get_book(db: Session, book_id: int) -> DBBook:
    statement = select(models.DBBook).where(models.DBBook.id == book_id)
    return db.exec(statement).one()


def create_book(db: Session, book: shemas.BookCreate) -> DBBook:
    db_book = DBBook(
        title=book.title,
        summary=book.summary,
        publication_date=book.publication_date,
        author_id=book.author_id,
    )
    db.add(db_book)
    db.commit()
    return db_book


def get_authors(db: Session, limit: int, page: int) -> Sequence[DBAuthor]:
    statement = select(models.DBAuthor).limit(limit).offset((page - 1) * limit)
    return db.exec(statement).all()


def get_author(db: Session, author_id: int) -> DBAuthor:
    statement = select(models.DBAuthor).where(models.DBAuthor.id == author_id)
    return db.exec(statement).one()


def create_author(db: Session, author: shemas.AuthorCreate) -> DBAuthor:
    db_author = DBAuthor(
        name=author.name,
        bio=author.bio,

    )
    db.add(db_author)
    db.commit()
    return db_author


def get_books_by_author(db: Session, author_id: int) -> Sequence[DBBook]:
    statement = (select(models.DBBook)
                 .where(models.DBBook.author_id == author_id))
    return db.exec(statement).all()
