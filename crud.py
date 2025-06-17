from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List, Optional

import models
import schemas


def get_author(db: Session, author_id: int):
    return db.query(models.Author).filter(models.Author.id == author_id).first()


def get_author_by_name(db: Session, name: str):
    search_name_lower = name.lower()
    result = db.query(models.Author).filter(func.lower(models.Author.name) == search_name_lower).first()
    return result


def get_authors(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Author).offset(skip).limit(limit).all()


def create_author(db: Session, author: schemas.AuthorCreate):
    existing_author = get_author_by_name(db, name=author.name)
    if existing_author:
                return None
        
    db_author = models.Author(name=author.name, bio=author.bio)
    db.add(db_author)
    db.commit()
    db.refresh(db_author)
    return db_author


def get_book(db: Session, book_id: int):
    return db.query(models.Book).filter(models.Book.id == book_id).first()


def get_books(db: Session, skip: int = 0, limit: int = 100, author_id: Optional[int] = None):
    query = db.query(models.Book)
    if author_id:
        query = query.filter(models.Book.author_id == author_id)
    return query.offset(skip).limit(limit).all()


def create_book(db: Session, book: schemas.BookCreate, author_id: int):
    db_book = models.Book(
        title=book.title,
        summary=book.summary,
        publication_date=book.publication_date,
        author_id=author_id
    )
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book
