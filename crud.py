from sqlalchemy.orm import Session
from typing import List, Optional, Type

import models
import schemas
from models import DBBook, DBAuthor


def create_author(db: Session, author: schemas.AuthorCreate) -> models.DBAuthor:
    db_author = models.DBAuthor(
        name=author.name,
        bio=author.bio
    )
    db.add(db_author)
    db.commit()
    db.refresh(db_author)
    return db_author


def get_all_authors(db: Session, skip: int = 0, limit: int = 10) -> list[Type[DBAuthor]]:
    return db.query(models.DBAuthor).offset(skip).limit(limit).all()


def get_author_by_id(db: Session, author_id: int) -> Optional[models.DBAuthor]:
    return db.query(models.DBAuthor).filter(models.DBAuthor.id == author_id).first()


def create_book(db: Session, book: schemas.BookCreate) -> models.DBBook:
    db_book = models.DBBook(
        title=book.title,
        summary=book.summary,
        publication_date=book.publication_date,
        author_id=book.author_id
    )
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book


def get_all_books(db: Session, skip: int = 0, limit: int = 10, author_id: Optional[int] = None) -> list[Type[DBBook]]:
    query = db.query(models.DBBook)
    if author_id:
        query = query.filter(models.DBBook.author_id == author_id)
    return query.offset(skip).limit(limit).all()
