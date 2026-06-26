from sqlalchemy import select
from sqlalchemy.orm import Session

import models
from models import DBAuthor, DBBook
from schemas import CreateAuthor, CreateBook


def get_all_authors(
        db: Session,
        skip: int = 0,
        limit: int = 10
):
    return db.scalars(
        select(models.DBAuthor)
        .offset(skip)
        .limit(limit)
    ).all()


def get_author(db: Session, author_id: int):
    return (
        db.scalars(
            select(models.DBAuthor)
            .where(models.DBAuthor.id == author_id)
        ).first()
    )


def get_author_by_name(db: Session, author_name: str):
    return (
        db.scalars(
            select(DBAuthor)
            .where(DBAuthor.name == author_name)
        ).first()
    )


def create_author(db: Session, author: CreateAuthor):
    db_author = models.DBAuthor(
        name=author.name,
        bio=author.bio,
    )
    db.add(db_author)
    db.commit()
    db.refresh(db_author)

    return db_author


def get_all_books(
        db: Session,
        skip: int = 0,
        limit: int = 100,
        author_id: int | None = None,
):
    queryset = select(models.DBBook).offset(skip).limit(limit)

    if author_id is not None:
        queryset = (
            queryset.where(models.DBBook.author_id == author_id)
        )
    return db.scalars(queryset).all()


def get_book_by_title(db: Session, book_title: str):
    return (
        db.scalars(
            select(DBBook)
            .where(DBBook.title == book_title)
        ).first()
    )


def create_book(db: Session, book: CreateBook):
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
