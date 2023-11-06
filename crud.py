from sqlalchemy.orm import Session

import models
from models import DBAuthor
from schemas import AuthorCreate, BookCreate, Book


def get_all_authors(db: Session, skip: int = 0, limit: int = 10):
    return db.query(DBAuthor).offset(skip).limit(limit).all()


def get_author_by_name(db: Session, name: str):
    return db.query(DBAuthor).filter(models.DBAuthor.name == name).first()


def get_author(db: Session, author_id: int):
    return db.query(DBAuthor).filter(models.DBAuthor.id == author_id).first()


def create_author(db: Session, author: AuthorCreate):
    db_author = models.DBAuthor(name=author.name, bio=author.bio)
    db.add(db_author)
    db.commit()
    db.refresh(db_author)
    return db_author


def create_book(db: Session, book: BookCreate):
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


def get_all_books(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.DBBook).offset(skip).limit(limit).all()


def get_books_by_author(
    db: Session, author_id: int, skip: int = 0, limit: int = 10
):
    return (
        db.query(models.DBBook)
        .filter(models.DBBook.author_id == author_id)
        .offset(skip)
        .limit(limit)
        .all()
    )
