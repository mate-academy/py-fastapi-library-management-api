from sqlalchemy.orm import Session
from sqlalchemy import select

import models
import schemas


def create_author(db: Session, author: schemas.AuthorCreate) -> models.Author:
    db_author = models.Author(**author.model_dump())
    db.add(db_author)
    db.commit()
    db.refresh(db_author)
    return db_author


def get_author(db: Session, author_id: int) -> models.Author | None:
    author = db.get(models.Author, author_id)
    return author


def get_authors(db: Session, skip: int = 0, limit: int = 100) -> list[models.Author]:
    stmt = select(models.Author).offset(skip).limit(limit).order_by(models.Author.id)
    result = db.scalars(stmt)
    authors = result.all()
    return authors


def create_book(
    db: Session,
    book: schemas.BookCreate,
    author_id: int
) -> models.Book:
    db_book = models.Book(**book.model_dump(), author_id=author_id)
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book


def get_book(db: Session, book_id: int) -> models.Book | None:
    book = db.get(models.Book, book_id)
    return book


def get_books(db: Session, skip: int = 0, limit: int = 100) -> list[models.Book]:
    stmt = select(models.Book).offset(skip).limit(limit).order_by(models.Book.id)
    result = db.scalars(stmt)
    books = result.all()
    return books


def get_books_by_author(
        db: Session,
        author_id: int,
        skip: int = 0,
        limit: int = 100
) -> list[models.Book]:
    stmt = (
        select(models.Book)
        .where(models.Book.author_id == author_id)
        .offset(skip)
        .limit(limit)
        .order_by(models.Book.id)
    )
    result = db.scalars(stmt)
    books = result.all()
    return books
