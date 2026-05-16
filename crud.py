from fastapi import Query
from sqlalchemy import select
from sqlalchemy.orm import Session

import models
from schemas import AuthorCreate, BookCreate


def get_all_authors(
    db: Session,
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=9, ge=1)
    ):

    return db.scalars(select(models.Author)).offset(skip).limit(limit).all()


def get_author(
    db: Session,
    author_id: int
):
    return db.scalar(select(models.Author).where(models.Author.id == author_id))


def create_author(db: Session, author: AuthorCreate):
    db_author = models.Author(
        name=author.name,
        bio=author.bio,
    )
    db.add(db_author)
    db.commit()
    db.refresh(db_author)

    return db_author


def get_all_books(db: Session,
    author_id: int | None = None,
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=9, ge=1)
    ):
    queryset = select(models.Book)

    if author_id is not None:
        queryset = queryset.join(models.Author).where(models.Author.id == author_id)

    return db.scalars(queryset).offset(skip).limit(limit).all()


def get_book(db: Session, book_id: int):
    return db.scalar(select(models.Book).where(models.Book.id == book_id))


def create_book(db: Session, book: BookCreate):
    db_book = models.Book(
        title=book.title,
        summary=book.summary,
        publication_date=book.publication_date,
        author_id=book.author_id,
    )
    db.add(db_book)
    db.commit()
    db.refresh(db_book)

    return db_book
