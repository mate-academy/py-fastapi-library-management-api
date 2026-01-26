from sqlalchemy import select
from sqlalchemy.orm import Session

import models
import schemas


def get_authors(db: Session, skip: int = 0, limit: int = 10):
    stmt = select(models.Author).offset(skip).limit(limit)
    return db.scalars(stmt).all()


def get_author(db: Session, author_id: int):
    stmt = select(models.Author).where(models.Author.id == author_id)
    return db.scalar(stmt)


def create_author(db: Session, author: schemas.AuthorCreate):
    db_author = models.Author(
        name=author.name,
        bio=author.bio,
    )
    db.add(db_author)
    db.commit()
    db.refresh(db_author)
    return db_author


def get_books(db: Session, skip: int = 0, limit: int = 10):
    stmt = select(models.Book).offset(skip).limit(limit)
    return db.scalars(stmt).all()


def get_books_by_author(db: Session, author_id: int):
    stmt = select(models.Book).where(models.Book.author_id == author_id)
    return db.scalars(stmt).all()


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
