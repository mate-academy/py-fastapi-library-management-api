from sqlalchemy import select
from sqlalchemy.orm import Session

import models
import schemas


def get_all_authors(db: Session, skip: int = 0, limit: int = 100):
    return db.scalars(select(models.Author).offset(skip).limit(limit)).all()


def create_author(db: Session, author: schemas.AuthorCreate):
    db_author = models.Author(name=author.name, bio=author.bio)
    db.add(db_author)
    db.commit()
    db.refresh(db_author)
    return db_author


def get_author(db: Session, author_id: int):
    return (db.scalars(
        select(models.Author).
        where(models.Author.id == author_id)).
            first())


def get_all_books(db: Session,
                  author_id: int | None = None,
                  skip: int = 0,
                  limit: int = 100):
    queryset = select(models.Book).offset(skip).limit(limit)

    if author_id is not None:
        queryset = queryset.where(models.Book.author_id == author_id)

    return db.scalars(queryset).all()


def create_book(db: Session, book: schemas.BookCreate):
    db_book = models.Book(
        title=book.title,
        summary=book.summary,
        publication_date=book.publication_date,
        author_id=book.author_id)
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book
