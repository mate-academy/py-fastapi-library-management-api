from sqlalchemy.orm import Session

import schemas
from db import models


def get_all_authors(db: Session, skip: int = 0, limit: int = 100) -> list[models.Author]:
    return db.query(models.DBAuthor).offset(skip).limit(limit).all()


def create_authors(db: Session, author: schemas.AuthorCreate) -> models.Author:
    db_author = models.DBAuthor(
        name=author.name,
        bio=author.bio,
    )
    db.add(db_author)
    db.commit()
    db.refresh(db_author)

    return db_author


def get_author_by_id(db: Session, author_id: int) -> models.Author:
    return db.query(models.DBAuthor).filter(models.DBAuthor.id == author_id).first()


def get_all_books(
    db: Session,
    skip: int = 0,
    limit: int = 100,
    author_id: int = None
) -> list[models.Book]:
    queryset = db.query(models.DBBook)

    if author_id is not None:
        queryset = queryset.filter(models.DBBook.author_id == author_id)

    return queryset.offset(skip).limit(limit).all()


def create_book(db: Session, book: schemas.BookCreate) -> models.Book:
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


def get_book_by_id(db: Session, author_id: int) -> models.Book:
    return db.query(models.DBBook).filter(models.DBBook.author_id == author_id).first()
