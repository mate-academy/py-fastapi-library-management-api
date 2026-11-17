from typing import Sequence

from sqlalchemy import select
from sqlalchemy.orm import Session

from db.models import Author, Book
from schemas import AuthorCreate, BookCreate


def create_author(db: Session, author_data: AuthorCreate) -> Author:
    author = Author(**author_data.model_dump())
    db.add(author)

    db.commit()
    db.refresh(author)
    return author


def list_of_authors(db: Session, skip: int, limit: int) -> Sequence[Author]:
    return db.scalars(select(Author).offset(skip).limit(limit)).all()


def get_author_by_id(db: Session, author_id: int) -> Author | None:
    return db.get(Author, author_id)


def get_author_by_name(db: Session, name: str) -> Author | None:
    return db.scalar(select(Author).where(Author.name == name))


def create_book(db: Session, book_data: BookCreate) -> Book:
    book = Book(**book_data.model_dump())
    db.add(book)

    db.commit()
    db.refresh(book)
    return book


def list_of_books(
    db: Session, author_id: int | None = None, skip: int = 0, limit: int = 100
) -> Sequence[Book]:
    stmt = select(Book).offset(skip).limit(limit)

    if author_id is not None:
        stmt = stmt.where(Book.author_id == author_id)

    return db.scalars(stmt).all()


def get_book(db: Session, book_id: int) -> Book | None:
    return db.get(Book, book_id)
