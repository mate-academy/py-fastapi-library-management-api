from sqlalchemy.orm import Session

from db import models
from schemas import AuthorBaseCreate, BookBaseCreate


def get_authors(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.DBAuthor).offset(skip).limit(limit).all()


def get_author_by_name(db: Session, name: str):
    return db.query(models.DBAuthor).filter(models.DBAuthor.name == name).first()


def create_author(db: Session, author: AuthorBaseCreate):
    db_author = models.DBAuthor(
        name=author.name,
        bio=author.bio,
    )
    db.add(db_author)
    db.commit()
    db.refresh(db_author)
    return db_author


def get_books(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.DBBook).offset(skip).limit(limit).all()


def get_book_by_title(db: Session, title: str):
    return db.query(models.DBBook).filter(models.DBBook.title == title).first()


def create_book(db: Session, book: BookBaseCreate):
    db_book = models.DBBook(
        title=book.title,
        summary=book.summary,
        publication_date=book.publication_date,
        author_id=book.author_id,
    )
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book
