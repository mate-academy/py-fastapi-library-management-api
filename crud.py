from sqlalchemy.orm import Session

import schemas
from db import models
from db.models import Author, Book


def get_all_authors(
        db: Session,
        skip: int = 0,
        limit: int = 10
) -> list[Author] | None:
    return db.query(models.Author).offset(skip).limit(limit).all()


def get_single_author(
        db: Session,
        author_id: int
) -> Author | None:
    return db.query(models.Author).filter(
        models.Author.id == author_id
    ).first()


def get_author_name(db: Session, name: str) -> Author | None:
    return (
        db.query(models.Author).filter(models.Author.name == name).first()
    )


def create_author(db: Session, author: schemas.AuthorCreate) -> Author:
    db_author = models.Author(
        name=author.name,
        bio=author.bio
    )
    db.add(db_author)
    db.commit()
    db.refresh(db_author)
    return db_author


def get_all_books(
        db: Session,
        author_id: int | None = None,
        skip: int = 0,
        limit: int = 100
) -> list[Book] | None:
    queryset = db.query(models.Book)

    if author_id is not None:
        queryset = queryset.filter(
            models.Book.author_id == author_id
        )

    return queryset.offset(skip).limit(limit).all()


def create_book(db: Session, book: schemas.BookCreate) -> Book:
    db_book = models.Book(
        title=book.title,
        summary=book.summary,
        author_id=book.author_id
    )
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book
