from typing import List

from sqlalchemy.orm import Session

import schemas
from db import models


def all_authors(
        db: Session, limit: int = 10, skip: int = 0
) -> List[models.Author]:
    authors = db.query(models.Author).offset(skip).limit(limit).all()

    return authors


def get_single_author_by_id(db: Session, author_id: int) -> models.Author:
    author = db.query(models.Author).filter(models.Author.id == author_id).first()

    return author


def get_author_by_name(db: Session, name: str) -> models.Author:
    author = db.query(models.Author).filter(models.Author.name == name).first()

    return author


def create_author(db: Session, author: schemas.AuthorCreate) -> models.Author:
    db_author = models.Author(
        name=author.name, bio=author.bio
    )
    db.add(db_author)
    db.commit()
    db.refresh(db_author)

    return db_author


def all_books(
        db: Session,
        limit: int = 10,
        skip: int = 0,
        author_id: int = None
) -> List[models.Book]:
    queryset = db.query(models.Book)

    if author_id is not None:
        queryset = queryset.filter(models.Author.id == author_id)

    return queryset.offset(skip).limit(limit).all()


def create_book(db: Session, book: schemas.BookCreate) -> models.Book:
    db_book = models.Book(
        title=book.title,
        summary=book.summary,
        publication_date=book.publication_date,
        author_id=book.author_id
    )
    db.add(db_book)
    db.commit()
    db.refresh(db_book)

    return db_book
