from typing import List

from sqlalchemy.orm import Session

import models
import schemas


def get_all_author(
        db: Session, skip: int | None, limit: int | None
) -> List[models.Author]:
    queryset = db.query(models.Author)
    if skip:
        queryset = queryset.offset(skip)
    if limit:
        queryset = queryset.limit(limit)
    return queryset.all()


def get_author_by_id(db: Session, author_id: int) -> models.Author:
    return (
        db.query(models.Author).filter(models.Author.id == author_id).first()
    )


def create_author(db: Session, author: schemas.AuthorCreate) -> models.Author:
    db_author = models.Author(**author.model_dump())
    db.add(db_author)
    db.commit()
    db.refresh(db_author)

    return db_author


def get_all_book(
    skip: int | None, limit: int | None, author_id: int | None, db: Session
) -> List[models.Book]:
    queryset = db.query(models.Book)
    if author_id:
        queryset = queryset.filter(models.Book.author_id == author_id)
    if skip:
        queryset = queryset.offset(skip)
    if limit:
        queryset = queryset.limit(limit)
    return queryset.all()


def create_book(db: Session, book: schemas.BookCreate) -> models.Book:
    db_book = models.Book(**book.model_dump())
    db.add(db_book)
    db.commit()
    db.refresh(db_book)

    return db_book
