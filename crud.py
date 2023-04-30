from typing import Optional, List

from sqlalchemy.orm import Session
from db import models
from schemas import AuthorCreate, BookCreate


def get_all_books(db: Session, skip: int = 0, limit: int = 10, author_id: int | None = None):
    query = db.query(models.DBBook)
    if author_id is not None:
        query = query.filter(models.DBBook.author_id == author_id)
    return query.offset(skip).limit(limit).all()


def create_book(db: Session, book: BookCreate):
    db_book = models.DBBook(
        title=book.title,
        summary=book.summary,
        publication_date=book.publication_date,
        author_id=book.author_id
    )
    db.add(db_book)
    db.commit()
    db.refresh(db_book)

    return db_book


def get_book_count(db: Session, skip: Optional[int] = 0, limit: Optional[int] = 10):
    query = db.query(models.DBBook).offset(skip).limit(limit)
    count = query.count()
    return count


def get_all_authors(db: Session, skip: int = 0, limit: int = 10):
    db.query(models.DBAuthor).offset(skip).limit(limit).all()
    return db.query(models.DBAuthor).offset(skip).limit(limit).all()


def get_author_count(db: Session, skip: Optional[int] = 0, limit: Optional[int] = 10):
    query = db.query(models.DBAuthor).offset(skip).limit(limit)
    count = query.count()
    return count


def create_author(db: Session, author: AuthorCreate):
    db_author = models.DBAuthor(
        name=author.name,
        bio=author.bio
    )
    db.add(db_author)
    db.commit()
    db.refresh(db_author)

    return db_author


def get_author(db: Session, author_id: int):
    return db.query(models.DBAuthor).filter(models.DBAuthor.id == author_id).first()
