from sqlalchemy.orm import Session
from typing import List, Optional

import models
import schema

def get_all_authors(db: Session) -> List[models.Author]:
    return db.query(models.Author).all()


def get_author_by_id(db: Session, author_id: int) -> Optional[models.Author]:
    return db.query(models.Author).filter(
        models.Author.id == author_id
    ).first()


def create_new_author(db: Session, author: schema.AuthorCreate) -> models.Author:
    db_author = models.Author(
        name=author.name,
        bio=author.bio
    )
    db.add(db_author)
    db.commit()
    db.refresh(db_author)
    return db_author


def get_all_books(db: Session, skip: int = 0, limit: int = 10) -> List[models.Book]:
    query = db.query(models.Book)
    return query.offset(skip).limit(limit).all()


def get_book_by_id(db: Session, book_id: int) -> Optional[models.Book]:
    return db.query(models.Book).filter(
        models.Book.id == book_id
    ).first()


def create_new_book(db: Session, book: schema.BookCreate) -> models.Book:
    db_book = models.Book(
        title=book.title,
        description=book.description,
        publication_date=book.publication_date,
        author_id=book.author_id,
    )
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book
