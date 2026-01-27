from sqlalchemy import select
from sqlalchemy.orm import Session

from models import Author, Book
from schemas import (
    AuthorCreateSchema,
    BookCreateSchema,
)


def get_all_authors(
    db: Session,
    to_skip: int,
    to_limit: int
) -> list[Author]:
    queryset = select(Author).offset(to_skip).limit(to_limit)
    return list(db.scalars(queryset).all())


def get_author(db: Session, author_id: int) -> Author:
    return db.scalar(select(Author).where(Author.id == author_id))


def create_author(db: Session, author_data: AuthorCreateSchema) -> Author:
    db_author = Author(**author_data.model_dump())
    db.add(db_author)
    db.commit()
    db.refresh(db_author)

    return db_author


def get_all_books(
    db: Session,
    to_skip: int,
    to_limit: int,
    author_id: int
) -> list[Book]:
    queryset = select(Book).offset(to_skip).limit(to_limit)

    if author_id:
        queryset = queryset.where(Book.author_id == author_id)
    return list(db.scalars(queryset).all())


def create_book(db: Session, book_data: BookCreateSchema) -> Book:
    db_book = Book(**book_data.model_dump())
    db.add(db_book)
    db.commit()
    db.refresh(db_book)

    return db_book
