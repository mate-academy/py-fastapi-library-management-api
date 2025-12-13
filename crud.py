from sqlalchemy import select
from sqlalchemy.orm import Session

import schemas
from db import models


def get_all_authors(db: Session, skip: int, limit: int) -> list[models.Author]:
    return db.scalars(select(models.Author)).offset(skip).limit(limit).all()


def get_author_by_id(db: Session,
                     author_id: int) -> models.Author | None:
    return db.scalar(
        select(models.Author).where(models.Author.id == author_id)
    )


def get_author_by_name(db: Session,
                     author_name: str) -> models.Author | None:
    return db.scalar(
        select(models.Author).where(models.Author.name == author_name)
    )


def create_author(db: Session, author: schemas.AuthorCreateSchema) -> models.Author:
    db_author = models.Author(
        name=author.name,
        bio=author.bio,
    )
    db.add(db_author)
    db.commit()
    db.refresh(db_author)

    return db_author


def get_all_books(
        db: Session,
        skip: int,
        limit: int,
        author_id: int | None = None,
) -> list[models.Book]:
    stmt = select(models.Book)
    if author_id:
        stmt = stmt.where(models.Book.author_id == author_id)

    return db.scalars(stmt).offset(skip).limit(limit).all()


def get_book_by_id(db: Session, book_id: int) -> models.Book | None:
    return db.scalar(
        select(models.Book).where(models.Book.id == book_id)
    )


def create_book(db: Session, book: schemas.BookCreateSchema) -> models.Book:
    db_book = models.Book(
        title=book.title,
        author_id=book.author_id,
        summary=book.summary,
        publication_date=book.publication_date,
    )
    db.add(db_book)
    db.commit()
    db.refresh(db_book)

    return db_book