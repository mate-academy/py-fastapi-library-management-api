from sqlalchemy import select
from sqlalchemy.orm import Session

import schemas
import models


def get_author_list(db: Session, skip: int = 0, limit: int = 10):
    queryset = select(models.Author).offset(skip).limit(limit)
    return db.scalars(queryset).all()


def get_author(db: Session, author_id: int):
    return db.scalar(select(models.Author).where(models.Author.id == author_id))


def create_author(db: Session, author: schemas.AuthorCreate):
    db_auhtor = models.Author(name=author.name, bio=author.bio)

    db.add(db_auhtor)
    db.commit()
    db.refresh(db_auhtor)

    return db_auhtor


def get_book_list(
    db: Session, author_id: int | None = None, skip: int = 0, limit: int = 10
):
    queryset = select(models.Book).offset(skip).limit(limit)

    if author_id is not None:
        queryset = queryset.join(models.Author).where(models.Author.id == author_id)

    return db.scalars(queryset).all()


def create_book(db: Session, book: schemas.BookCreate):
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
