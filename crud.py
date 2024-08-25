from typing import List, Optional

from sqlalchemy.orm import Session
from db import models
import schemas


def get_all_books(
        db: Session, skip: int = 0,
        limit: int = 5
) -> List[models.Book]:
    return db.query(models.Book).offset(skip).limit(limit).all()


def get_books_by_author_id(db: Session, author_id: int) -> List[models.Book]:
    return (
        db.query(models.Book).filter(models.Book.author_id == author_id).all()
    )


def get_book_by_title(db: Session, title: str) -> Optional[models.Book]:
    return db.query(models.Book).filter(models.Book.title == title).first()


def create_book(db: Session, book: schemas.BookCreate) -> models.Book:

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


def create_author(db: Session, author: schemas.AuthorCreate) -> models.Author:
    db_author = models.Author(name=author.name, bio=author.bio)
    db.add(db_author)
    db.commit()
    db.refresh(db_author)

    return db_author


def get_all_authors(
        db: Session,
        skip: int = 0,
        limit: int = 5
) -> List[models.Author]:
    return db.query(models.Author).offset(skip).limit(limit).all()


def get_author_by_id(db: Session, author_id: int) -> Optional[models.Author]:
    return (
        db.query(models.Author).filter(models.Author.id == author_id).first()
    )
