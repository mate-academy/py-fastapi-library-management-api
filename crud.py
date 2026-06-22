from sqlalchemy import select
from sqlalchemy.orm import Session

import models
import schema


def get_author(db: Session, author_id: int):
    return db.get(models.Author, author_id)


def get_authors(db: Session, skip: int = 0, limit: int = 100):
    statement = select(models.Author).offset(skip).limit(limit)
    return db.execute(statement).scalars().all()


def create_author(db: Session, author: schema.AuthorCreate):
    db_author = models.Author(name=author.name, bio=author.bio)
    db.add(db_author)
    db.commit()
    db.refresh(db_author)
    return db_author


def get_books(db: Session, skip: int = 0, limit: int = 100, author_id: int | None = None):
    statement = select(models.Book)
    if author_id is not None:
        statement = statement.where(models.Book.author_id == author_id)
    statement = statement.offset(skip).limit(limit)
    return db.execute(statement).scalars().all()


def create_book(db: Session, book: schema.BookCreate, author_id: int):
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
