from typing import List, Optional

from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError

import models
import schemas


def get_all_authors(
        db: Session,
        skip: int = 0,
        limit: int = 10
) -> List[models.Author]:
    return db.query(models.Author).offset(skip).limit(limit).all()


def get_author_by_name(
        db: Session,
        name: str
) -> Optional[models.Author]:
    return (
        db.query(models.Author).filter(models.Author.name == name).first()
    )


def create_author(
        db: Session,
        author: schemas.AuthorCreate
) -> models.Author:
    try:
        db_author = models.Author(
            name=author.name,
            bio=author.bio,
        )
        db.add(db_author)
        db.commit()
        db.refresh(db_author)

        return db_author
    except SQLAlchemyError as e:
        db.rollback()
        print(f"While creating this author, an error has occurred: {e}")


def get_author(
        db: Session,
        author_id: int
) -> Optional[models.Author]:
    return db.query(models.Author).filter(models.Author.id == author_id).first()


def get_book_list(
        db: Session,
        author_id: int | None = None,
        skip: int = 0,
        limit: int = 10
) -> List[models.Book]:
    queryset = db.query(models.Book).offset(skip).limit(limit)

    if author_id:
        queryset = queryset.filter(models.Book.author_id == author_id)

    return queryset


def get_book(db: Session, book_id: int) -> Optional[models.Book]:
    return db.query(models.Book).filter(models.Book.id == book_id).first()


def create_book(db: Session, book: schemas.BookCreate) -> models.Book:
    try:
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
    except SQLAlchemyError as e:
        db.rollback()  # Відкат транзакції у разі помилки
        print(f"While creating the book, an error has occurred: {e}")
