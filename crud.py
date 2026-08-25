from sqlalchemy import select
from sqlalchemy.orm import Session

import models
import schemas


def get_all_books(
        db: Session,
        skip: int = 0,
        limit: int = 100,
):
    return db.scalars(
        select(models.Book).offset(skip).limit(limit)
    ).all()


def get_book_by_id(db: Session, book_id: int):
    return db.scalar(
        select(models.Book).where(models.Book.id == book_id)
    )


def get_book_by_title(db: Session, title: str):
    return db.scalar(
        select(models.Book).where(models.Book.title == title)
    )


def create_book(db: Session, book: schemas.BookCreate, author_id: int):
    db_book = models.Book(
        title=book.title,
        summary=book.summary,
        publication_date=book.publication_date,
        author_id=author_id,
    )
    db.add(db_book)
    db.commit()
    db.refresh(db_book)

    return db_book


def get_all_authors(
        db: Session,
        skip: int = 0,
        limit: int = 100,
):
    return db.scalars(
        select(models.Author).offset(skip).limit(limit)
    ).all()


def get_author_by_id(db: Session, author_id: int):
    return db.scalar(
        select(models.Author).where(models.Author.id == author_id)
    )


def get_author_by_name(db: Session, name: str):
    return db.scalar(
        select(models.Author).where(models.Author.name == name)
    )


def create_author(db: Session, author: schemas.AuthorCreate):
    db_author = models.Author(
        name=author.name,
        bio=author.bio,
    )

    db.add(db_author)
    db.commit()
    db.refresh(db_author)

    return db_author


def get_book_list(
        db: Session,
        title: str | None = None,
        author_id: int | None = None,
        skip: int = 0,
        limit: int = 100,
):

    queryset = select(models.Book)

    if author_id is not None:
        queryset = (
            queryset.where(models.Book.author_id == author_id)
        )

    if title is not None:
        queryset = queryset.where(models.Book.title == title)

    queryset = queryset.offset(skip).limit(limit)

    return db.scalars(queryset).all()
