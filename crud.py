from sqlalchemy.orm import Session

import schemas
from db import models


def get_author_list(db: Session, skip: int, limit: int) -> list[models.Author]:
    db_authors = db.query(models.Author).offset(skip).limit(limit).all()

    return db_authors


def get_author_count(db: Session) -> int:
    return db.query(models.Author).count()


def get_author_by_id(db: Session, author_id: int) -> models.Author | None:
    return db.query(models.Author).filter_by(id=author_id).first()


def create_author(db: Session, author: schemas.AuthorCreate):
    new_author = models.Author(
        name=author.name,
        bio=author.bio,
    )

    db.add(new_author)
    db.commit()
    db.refresh(new_author)

    return new_author


def get_book_list(
    db: Session, skip: int, limit: int, author_id: int = None
) -> list[models.Book]:
    queryset = db.query(models.Book)

    if author_id is not None:
        queryset = queryset.filter_by(author_id=author_id)

    return queryset.offset(skip).limit(limit).all()


def get_book_count(db: Session) -> int:
    return db.query(models.Book).count()


def create_book(db: Session, book: schemas.BookCreate):
    new_book = models.Book(
        title=book.title,
        summary=book.summary,
        publication_date=book.publication_date,
        author_id=book.author_id,
    )

    db.add(new_book)
    db.commit()
    db.refresh(new_book)

    return new_book
