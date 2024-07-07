# crud.py
from sqlalchemy.orm import Session
import models
import schemas
from typing import List, Optional


def get_author(db: Session, author_id: int) -> Optional[models.Author]:
    return db.query(models.Author).filter(models.Author.id == author_id).first()


def get_author_by_name(db: Session, name: str) -> Optional[models.Author]:
    return db.query(models.Author).filter(models.Author.name == name).first()


def get_authors(db: Session, skip: int = 0, limit: int = 10) -> List[type[models.Author]]:
    return db.query(models.Author).offset(skip).limit(limit).all()


def create_author(db: Session, author: schemas.AuthorCreate) -> models.Author:
    db_author = models.Author(name=author.name, bio=author.bio)
    db.add(db_author)
    db.commit()
    db.refresh(db_author)
    return db_author


def get_books(db: Session, skip: int = 0, limit: int = 10) -> List[type[models.Book]]:
    return db.query(models.Book).offset(skip).limit(limit).all()


def get_books_by_author(db: Session, author_id: int, skip: int = 0, limit: int = 10) -> List[type[models.Book]]:
    return db.query(models.Book).filter(models.Book.author_id == author_id).offset(skip).limit(limit).all()


def create_book(db: Session, book: schemas.BookCreate) -> models.Book:
    db_book = models.Book(
        title=book.title,
        summary=book.summary,
        publication_date=book.publication_date,
        author_id=book.author_id
    )
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book
