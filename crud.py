from typing import List

from sqlalchemy.orm import Session

import schemas
from db import models


def get_all_authors(db: Session) -> List[schemas.Author]:
    return db.query(models.Author)


def create_author(db: Session, author: schemas.AuthorCreate) -> schemas.Author:
    db_author = models.Author(name=author.name, bio=author.bio)
    db.add(db_author)
    db.commit()
    db.refresh(db_author)
    return db_author


def get_author(db: Session, author_id: int) -> schemas.Author:
    author = (db.query(models.Author)
              .filter(models.Author.id == author_id).first())
    return author


def create_book(db: Session, book: schemas.BookCreate) -> schemas.Book:
    db_book = models.Book(
        title=book.title,
        summary=book.summary,
        publication_date=book.publication_date,
        author_id=book.author_id,
    )
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book


def get_all_books(db: Session) -> List[models.Book]:
    return db.query(models.Book)


def get_book(db: Session, book_id: int) -> schemas.Book:
    book = db.query(models.Book).filter(models.Book.id == book_id).first()
    return book
