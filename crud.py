from __future__ import annotations

from sqlalchemy.orm import Session

import models
import schemas


def get_author(db: Session, author_id: int) -> models.Author | None:
    return db.query(models.Author
                    ).filter(models.Author.id == author_id).first()


def get_authors(
        db: Session,
        skip: int = 0,
        limit: int = 100
) -> list[models.Author]:
    return db.query(models.Author).offset(skip).limit(limit).all()


def get_author_by_name(db: Session, name: str) -> models.Author | None:
    return (
        db.query(models.Author).filter(models.Author.name == name).first()
    )


def create_author(db: Session, author: schemas.AuthorCreate) -> models.Author:
    db_author = models.Author(
        name=author.name,
        bio=author.bio,
    )
    db.add(db_author)
    db.commit()
    db.refresh(db_author)
    return db_author


def get_books(
        db: Session,
        author_id: int = None,
        skip: int = 0,
        limit: int = 100
) -> list[models.Book]:
    queryset = db.query(models.Book)
    if author_id:
        queryset = queryset.filter(models.Book.author_id == author_id)
    return queryset.offset(skip).limit(limit).all()


def create_book(db: Session, book: schemas.BookCreate) -> models.Book:
    db_book = models.Book(
        title=book.title,
        bio=book.bio,
        publication_date=book.publication_date,
        author_id=book.author_id
    )
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book
