from typing import Optional, List
from sqlalchemy.orm import Session
import schemas
import models


def create_author(db: Session, author: schemas.AuthorCreate) -> models.Author:
    db_author = models.Author(**author.model_dump())
    db.add(db_author)
    db.commit()
    db.refresh(db_author)
    return db_author


def get_author(db: Session, author_id: int) -> Optional[models.Author]:
    return db.get(models.Author, author_id)


def get_authors(db: Session, skip: int = 0, limit: int = 100) -> List[models.Author]:
    return db.query(models.Author).order_by(models.Author.id).offset(skip).limit(limit).all()


def create_book(db: Session, book: schemas.BookCreate, author_id: int) -> models.Book:
    db_book = models.Book(**book.model_dump(), author_id=author_id)
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book


def get_books(db: Session, skip: int = 0, limit: int = 100) -> List[models.Book]:
    return db.query(models.Book).order_by(models.Book.id).offset(skip).limit(limit).all()


def get_books_by_author(db: Session, author_id: int, skip: int = 0, limit: int = 100) -> List[models.Book]:
    return (
        db.query(models.Book)
        .filter(models.Book.author_id == author_id)
        .order_by(models.Book.id)
        .offset(skip)
        .limit(limit)
        .all()
    )
