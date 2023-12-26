from sqlalchemy.orm import Session

import schemas
from db import models


def get_all_authors(
        db: Session,
        limit: int = 5,
        offset: int = 0,

) -> list[schemas.Author]:

    return db.query(models.Author).limit(limit).offset(offset).all()


def get_author_name(db: Session, name: str) -> models.Author | None:
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


def get_book_list(
        db: Session,
        author_id: int | None = None,
        limit: int = 5,
        offset: int = 0,
) -> list[schemas.Book]:
    queryset = db.query(models.Book)

    if author_id:
        queryset = queryset.filter(
            models.Book.author_id == author_id
        )

    return queryset.limit(limit).offset(offset).all()


def get_book_by_title(db: Session, title: str) -> models.Book:
    return (
        db.query(models.Book).filter(models.Book.title == title).first()
    )


def get_book_by_author_id(db: Session, author_id: int) -> models.Book:
    return (
        db.query(models.Book).filter(models.Book.id == author_id).first()
    )


def get_book(db: Session, book_id: int) -> models.Author:
    return (
        db.query(models.Book).filter(models.Book.id == book_id).first()
    )


def create_book(db: Session, book: schemas.BookCreate) -> models.Book:
    db_book = models.Book(
        title=book.title,
        summary=book.summary,
        publication_date=book.publication_date,
        author_id=book.author_id,
    )
    db.add(db_book)
    db.commit()
    db.refresh(db_book)

    return db_book
