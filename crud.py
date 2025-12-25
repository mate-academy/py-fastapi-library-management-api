from sqlalchemy.orm import Session
from sqlalchemy import select

import schemas
from db import models


def get_author_list(db: Session, skip: int = 0, limit: int = 100):
    return db.scalars(select(models.DBAuthor).offset(skip).limit(limit)).all()


def get_author(db: Session, author_id: int):
    return db.scalar(
        select(models.DBAuthor
               ).where(models.DBAuthor.id == author_id))


def get_author_by_name(db: Session, name: str):
    return db.scalar(
        select(models.DBAuthor)
        .where(models.DBAuthor.name == name)
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
        author_id: int | None = None,
        skip: int = 0,
        limit: int = 100
):
    queryset = select(models.DBBook)

    if author_id is not None:
        queryset = queryset.where(models.DBBook.author_id == author_id)

    return db.scalars(queryset.offset(skip).limit(limit)).all()


def get_book(db: Session, book_id: int):
    return db.scalar(select(models.DBBook).where(models.DBBook.id == book_id))


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
