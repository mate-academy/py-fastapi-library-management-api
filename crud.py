from sqlalchemy import select
from sqlalchemy.orm import Session

import schemas
from db import models


def get_all_author(db: Session, skip: int = 0, limit: int = 10):
    return db.scalars(select(models.DBAuthor).offset(skip).limit(limit)).all()


def get_author_by_name(db: Session, name: str):
    return (
        db.scalars(select(models.DBAuthor).where(models.DBAuthor.name == name)).first()
    )


def get_author_by_id(db: Session, author_id: int):
    return db.scalars(
        select(models.DBAuthor).where(models.DBAuthor.id == author_id)
    ).first()


def create_author(db: Session, author: schemas.AuthorCreate):
    db_author = models.DBAuthor(
        name=author.name,
        bio=author.bio,
    )
    db.add(db_author)
    db.commit()
    db.refresh(db_author)

    return db_author


def get_all_book(db: Session, skip: int = 0, limit: int = 10):
    return db.scalars(select(models.DBBook).offset(skip).limit(limit)).all()


def get_book_by_id(db: Session, book_id: int):
    return db.scalars(select(models.DBBook).where(models.DBBook.id == book_id)).first()


def get_books_by_author_id(db: Session, author_id: int, skip: int = 0, limit: int = 10):
    return db.scalars(
        select(models.DBBook)
        .where(models.DBBook.author_id == author_id)
        .offset(skip)
        .limit(limit)
    ).all()


def create_book(db: Session, book: schemas.BookCreate, author_id: int):
    db_book = models.DBBook(
        title=book.title,
        summary=book.summary,
        author_id=author_id,
        publication_date=book.publication_date,
    )

    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book
