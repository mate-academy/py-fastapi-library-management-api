from sqlalchemy.orm import Session

import models
import schemas


def get_all_books(db: Session, skip: int = 0, limit: int = 100) -> list[models.Book]:
    return db.query(models.Book).offset(skip).limit(limit).all()


def get_book_by_id(db: Session, book_id: int) -> models.Book:
    return db.query(models.Book).get(book_id)


def filter_books_by_author(db: Session, author_id: int) -> list[models.Book]:
    return db.query(models.Book).filter(models.Book.author_id == author_id).all()


def create_book(db: Session, book: schemas.BookCreate) -> models.Book:
    db_book = models.Book(**book.dict())
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book


def get_all_authors(db: Session, skip: int = 0, limit: int = 100) -> list[models.Author]:
    return db.query(models.Author).offset(skip).limit(limit).all()


def get_author_by_id(db: Session, author_id: int) -> models.Author:
    return db.query(models.Author).get(author_id)


def create_author(db: Session, author: schemas.AuthorCreate) -> models.Author:
    db_author = models.Author(**author.dict())
    db.add(db_author)
    db.commit()
    db.refresh(db_author)
    return db_author
