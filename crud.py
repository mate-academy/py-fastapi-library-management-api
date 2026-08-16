from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError

import models
import schemas


def get_author(db: Session, author_id: int) -> Optional[models.Author]:
    return db.query(models.Author).filter(models.Author.id == author_id).first()


def get_authors(db: Session, skip: int = 0, limit: int = 100) -> List[models.Author]:
    return db.query(models.Author).offset(skip).limit(limit).all()


def create_author(db: Session, author: schemas.AuthorCreate) -> models.Author:
    db_author = models.Author(name=author.name, bio=author.bio)
    try:
        db.add(db_author)
        db.commit()
        db.refresh(db_author)
        return db_author
    except SQLAlchemyError:
        db.rollback()
        raise


def get_books(db: Session, skip: int = 0, limit: int = 100, author_id: Optional[int] = None) -> List[models.Book]:
    query = db.query(models.Book)
    if author_id is not None:
        query = query.filter(models.Book.author_id == author_id)
    return query.offset(skip).limit(limit).all()


def create_book_for_author(db: Session, book: schemas.BookCreate, author_id: int) -> models.Book:
    """
    Creates a book for a specific author.
    Raises ValueError if the author is not found (expected to be caught and converted to 404 in the API router).
    """
    db_author = get_author(db, author_id)
    if not db_author:
        raise ValueError(f"Author with id {author_id} not found")

    db_book = models.Book(**book.dict(), author_id=author_id)
    try:
        db.add(db_book)
        db.commit()
        db.refresh(db_book)
        return db_book
    except SQLAlchemyError:
        db.rollback()
        raise
