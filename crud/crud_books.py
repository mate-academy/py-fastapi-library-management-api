from sqlalchemy.orm import Session
from db import models
from schemas import schemas_books
from typing import Optional


def get_books(db: Session, skip: int = 0, limit: int = 10, author_id: Optional[int] = None):
    if author_id:
        return db.query(models.Book).filter(models.Book.author_id == author_id).offset(skip).limit(limit).all()
    return db.query(models.Book).offset(skip).limit(limit).all()


def get_books_id(db: Session, book_id: int = None):
    return db.query(models.Book).filter(models.Book.id == book_id).first()


def create_book(db: Session, create_books: schemas_books.CreateBooks):
    db_create_book = models.Book(
        title = create_books.title,
        summary = create_books.summary,
        publication_date = create_books.publication_date,
        author_id = create_books.author_id
    )
    db.add(db_create_book)
    db.commit()
    db.refresh(db_create_book)
    return db_create_book


def books_title(db: Session, title: str):
    return db.query(models.Book).filter(models.Book.title == title).first()