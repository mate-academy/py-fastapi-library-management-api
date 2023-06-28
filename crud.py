from typing import List

from fastapi import HTTPException
from sqlalchemy.orm import Session

import schemas, models


def get_author_by_name(db: Session, author_name: str) -> models.DBAuthor | None:
    return db.query(models.DBAuthor).filter(models.DBAuthor.name == author_name).first()


def get_author_by_id(db: Session, author_id: int) -> models.DBAuthor:
    author = db.query(models.DBAuthor).filter(models.DBAuthor.id == author_id).first()
    if not author:
        raise HTTPException(status_code=404, detail="Author not found")
    return author


def get_authors(db: Session, skip: int = 0, limit: int = 100) -> List[models.DBAuthor]:
    return db.query(models.DBAuthor).offset(skip).limit(limit).all()


def create_author(db: Session, author: schemas.AuthorCreate) -> models.DBAuthor:
    db_author = models.DBAuthor(name=author.name, bio=author.bio)
    db.add(db_author)
    db.commit()
    db.refresh(db_author)
    return db_author


def get_book(db: Session, book_title: str) -> models.DBBook | None:
    return db.query(models.DBBook).filter(models.DBBook.title == book_title).first()


def get_book_by_id(db: Session, book_id: int) -> models.DBBook:
    book = db.query(models.DBBook).filter(models.DBBook.id == book_id).first()
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return book


def get_books(db: Session, skip: int = 0, limit: int = 100) -> List[models.DBBook]:
    return db.query(models.DBBook).offset(skip).limit(limit).all()


def create_book(db: Session, book: schemas.BookCreate) -> models.DBBook:
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
