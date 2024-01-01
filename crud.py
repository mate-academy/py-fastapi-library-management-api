from typing import List

from sqlalchemy import select
from sqlalchemy.orm import Session

import schemas
from models import Author, Book


def get_author_list(db: Session, skip: int, limit: int) -> List[Author]:
    return db.execute(select(Author).offset(skip).limit(limit)).scalars()


def get_author_by_id(db: Session, author_id: int) -> Author:
    return db.execute(select(Author).where(Author.id == author_id)).scalar()


def get_author_by_name(db: Session, author_name: str) -> Author:
    return db.execute(
        select(Author).where(Author.name == author_name)
    ).scalar()


def create_author(
        db: Session, author: schemas.AuthorCreate | None = None
) -> Author:
    author = Author(name=author.name, bio=author.bio)

    db.add(author)
    db.commit()
    db.refresh(author)

    return author


def get_book_list(db: Session, skip: int = 0, limit: int = 5) -> List[Book]:
    return db.execute(select(Book).offset(skip).limit(limit)).scalars()


def filter_book_by_author_id(
        db: Session, author_id: int | None = None
) -> List[Book]:
    return db.execute(
        select(Book).where(Book.author_id == author_id)
    ).scalars().all()


def get_book_by_title(db: Session, book_title: str) -> Book:
    return db.execute(select(Book).where(Book.title == book_title)).scalar()


def create_book(db: Session, book: schemas.BookCreate) -> Book:
    book = Book(
        title=book.title,
        summary=book.summary,
        publication_date=book.publication_date,
        author_id=book.author_id,
    )

    db.add(book)
    db.commit()
    db.refresh(book)

    return book
