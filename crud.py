from unittest import skip

from sqlalchemy.dialects.mysql import limit
from sqlalchemy.orm import Session

import schemas
from db import models


def get_all_authors(
    db: Session,
    skip: int = 0,
    limit: int = 10,
):
    return (
        db.query(models.DBAuthor)
        .order_by(models.DBAuthor.id)
        .offset(skip)
        .limit(limit)
        .all()
    )

def get_author(db: Session, author_id: int):
    return (
        db.query(models.DBAuthor)
        .filter(models.DBAuthor.id == author_id)
        .first()
    )

def create_author(
        db: Session,
        author: schemas.AuthorCreate
):
    db_author = models.DBAuthor(
        name=author.name,
        bio=author.bio,
    )
    db.add(db_author)
    db.commit()
    db.refresh(db_author)
    return db_author

def get_all_books(
        db: Session,
        skip: int = 0,
        limit: int = 10,
        author_id: int | None = None,
):
    query = db.query(models.DBBook)
    if author_id is not None:
        query = query.filter(models.DBBook.author_id == author_id)
    return (
        query
        .order_by(models.DBBook.id)
        .offset(skip)
        .limit(limit)
        .all()
    )
    return db.query(models.DBBook).all()

def create_book(
        db: Session,
        book: schemas.BookCreate,
        author_id: int,
):
    db_book = models.DBBook(
        title=book.title,
        summary=book.summary,
        publication_date=book.publication_date,
        author_id=author_id,
    )
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book

