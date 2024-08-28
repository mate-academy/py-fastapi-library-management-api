from sqlalchemy.orm import Session
from typing import List, Optional

import models
import schema

def get_all_authors(db: Session) -> List[models.DBAuthor]:
    return db.query(models.DBAuthor).all()


def get_author_by_id(db: Session, author_id: int) -> Optional[models.DBAuthor]:
    return db.query(models.DBAuthor).filter(
        models.DBAuthor.id == author_id
    ).first()


def create_new_author(db: Session, author: schema.AuthorCreate) -> models.DBAuthor:
    db_author = models.DBAuthor(
        name=author.name,
        bio=author.bio
    )
    db.add(db_author)
    db.commit()
    db.refresh(db_author)
    return db_author


def get_all_books(db: Session, skip: int = 0, limit: int = 10) -> List[models.DBBook]:
    query = db.query(models.DBBook)
    return query.offset(skip).limit(limit).all()


def get_book_by_id(db: Session, book_id: int) -> Optional[models.DBBook]:
    return db.query(models.DBBook).filter(
        models.DBBook.id == book_id
    ).first()


def create_new_book(db: Session, book: schema.BookCreate) -> models.DBBook:
    db_book = models.DBBook(
        title=book.title,
        description=book.description,
        publication_date=book.publication_date,
        author_id=book.author_id,
    )
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book
