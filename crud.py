from typing import List, Optional

from sqlalchemy.orm import Session

import models
import schemas


def get_author(db: Session, author_id: int) -> Optional[models.Author]:
    return db.query(models.Author)\
        .filter(models.Author.id == author_id)\
        .first()


def get_author_by_name(db: Session, name: str) -> Optional[models.Author]:
    return db.query(models.Author).filter(models.Author.name == name).first()


def get_authors(
        db: Session,
        skip: int = 0,
        limit: int = 100
) -> List[models.Author]:
    return db.query(models.Author).offset(skip).limit(limit).all()


def create_author(db: Session, author: schemas.AuthorCreate) -> models.Author:
    db_author = models.Author(
        name=author.name,
        bio=author.bio
    )
    db.add(db_author)
    db.commit()
    db.refresh(db_author)
    return db_author


def get_books(
        db: Session,
        skip: int = 0,
        limit: int = 100,
        author_id: int | None = None
) -> List[models.Book]:
    queryset = db.query(models.Book)
    if author_id is not None:
        queryset = queryset.filter(
            models.Book.author_id == author_id
        )

    return queryset.offset(skip).limit(limit).all()


def get_book_by_title(db: Session, title: str) -> Optional[models.Book]:
    return db.query(models.Book).filter(models.Book.title == title).first()


def create_author_book(
        db: Session,
        book: schemas.BookCreate,
        author_id: int
) -> models.Book:
    db_book = models.Book(
        **book.model_dump(),
        author_id=author_id
    )
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book
