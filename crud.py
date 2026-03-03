from sqlalchemy import select, Sequence
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session, selectinload

import models
import schemas


class AlreadyExists(Exception):
    pass


class IncorrectFK(Exception):
    pass


def get_authors_list(
    db: Session, skip: int = 0, limit: int = 100
) -> Sequence[models.Author]:
    return db.scalars(
        select(models.Author)
        .options(
            selectinload(models.Author.books).load_only(models.Book.title)
        )
        .offset(skip)
        .limit(limit)
    ).all()


def get_author_by_id(db: Session, author_id: int) -> models.Author:
    return db.scalar(
        select(models.Author).where(models.Author.id == author_id)
    )


def create_author(db: Session, author: schemas.AuthorCreate) -> models.Author:
    try:
        db_author = models.Author(**author.model_dump())
        db.add(db_author)
        db.commit()
        db.refresh(db_author)
    except IntegrityError:
        db.rollback()
        raise AlreadyExists()
    return db_author


def get_books_list(
    db: Session, author_id: int | None, skip: int = 0, limit: int = 100
) -> Sequence[models.Book]:
    stmt = select(models.Book)
    if author_id is not None:
        stmt = stmt.where(models.Book.author_id == author_id)
    return db.scalars(stmt.offset(skip).limit(limit))


def get_book_by_id(db: Session, book_id: int) -> models.Book:
    return db.scalar(select(models.Book).where(models.Book.id == book_id))


def create_book(db: Session, book: schemas.BookCreate) -> models.Book:
    try:
        db_book = models.Book(**book.model_dump())
        db.add(db_book)
        db.commit()
        db.refresh(db_book)
    except IntegrityError:
        db.rollback()
        raise IncorrectFK()
    return db_book
