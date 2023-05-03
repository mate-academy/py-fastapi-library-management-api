from typing import List, Optional

from sqlalchemy.orm import Session

from db import models
import schemas


def get_all_books(db: Session):
    return db.query(models.DBBook).all()


def get_book_by_title(db: Session, title: str):
    return db.query(models.DBBook).filter(models.DBBook.title == title).first()


def create_book(db: Session, book: schemas.BookCreate):
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


def get_books_by_author_id(
    db: Session, author_id: int, skip: int = 0, limit: int = 100
) -> List[schemas.Book]:
    books = (
        db.query(models.DBBook)
        .filter(models.DBBook.author_id == author_id)
        .offset(skip)
        .limit(limit)
        .all()
    )
    return books


def get_all_authors(
    db: Session, skip: int = 0, limit: int = 100
) -> List[schemas.Author]:
    authors = db.query(models.DBAuthor).offset(skip).limit(limit).all()
    return authors


def get_author_by_name(db: Session, name: str):
    return (
        db.query(models.DBAuthor).filter(models.DBAuthor.name == name).first()
    )


def create_author(db: Session, author: schemas.AuthorCreate) -> schemas.Author:
    db_author = models.DBAuthor(name=author.name, bio=author.bio)
    db.add(db_author)
    db.commit()
    db.refresh(db_author)
    return db_author


def get_author(db: Session, author_id: int) -> Optional[schemas.Author]:
    author = (
        db.query(models.DBAuthor)
        .filter(models.DBAuthor.id == author_id)
        .first()
    )
    return author
