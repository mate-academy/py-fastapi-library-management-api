from typing import Optional

from sqlalchemy.orm import Session, Query

import schemas
from db import models
from schemas import AuthorCreate, BookCreate
from sqlalchemy import func, desc


def get_all_books(
        db: Session,
        skip: int = 0,
        limit: int = 10,
        author_id: int | None = None,
        title: str | None = None,
        sort_by: str | None = None
) -> Query:
    query = db.query(models.DBBook)
    if author_id is not None:
        query = query.filter(models.DBBook.author_id == author_id)
    if title is not None:
        query = query.filter(func.lower(models.DBBook.title).contains(title.lower()))
    if sort_by == 'title':
        query = query.order_by(models.DBBook.title)
    elif sort_by == 'date':
        query = query.order_by(desc(models.DBBook.publication_date))

    return query.offset(skip).limit(limit).all()


def create_book(db: Session, book: BookCreate):
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


def get_book_count(db: Session, skip: Optional[int] = 0, limit: Optional[int] = 10):
    query = db.query(models.DBBook).offset(skip).limit(limit)
    count = query.count()
    return count


def get_book(db: Session, book_id: int):
    return db.query(models.DBBook).filter(models.DBBook.id == book_id).first()


def update_book(db: Session, db_book: models.DBBook, book: schemas.BookUpdate):
    for field, value in book.dict(exclude_unset=True).items():
        setattr(db_book, field, value)
    db.commit()
    db.refresh(db_book)
    return db_book


def delete_book(db: Session, db_book: models.DBBook):
    db.delete(db_book)
    db.commit()


def get_all_authors(
        db: Session,
        skip: int = 0,
        limit: int = 10,
        name: str | None = None,
        sort_by: str | None = None
):
    query = db.query(models.DBAuthor)
    if name is not None:
        query = query.filter(func.lower(models.DBAuthor.name).contains(name.lower()))
    if sort_by == "name":
        query = query.order_by(models.DBAuthor.name)
    return query.offset(skip).limit(limit).all()


def get_author_count(db: Session, skip: Optional[int] = 0, limit: Optional[int] = 10):
    query = db.query(models.DBAuthor).offset(skip).limit(limit)
    count = query.count()
    return count


def create_author(db: Session, author: AuthorCreate):
    db_author = models.DBAuthor(
        name=author.name,
        bio=author.bio
    )
    db.add(db_author)
    db.commit()
    db.refresh(db_author)

    return db_author


def get_author(db: Session, author_id: int):
    return db.query(models.DBAuthor).filter(models.DBAuthor.id == author_id).first()


def update_author(db: Session, db_author: models.DBAuthor, author: schemas.AuthorUpdate):
    for field, value in author.dict(exclude_unset=True).items():
        setattr(db_author, field, value)
    db.commit()
    db.refresh(db_author)
    return db_author


def delete_author(db: Session, db_author: models.DBAuthor):
    db.delete(db_author)
    db.commit()
