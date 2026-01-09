from typing import Optional

from sqlalchemy import select
from sqlalchemy.orm import Session

from schemas import (
    AuthorCreate,
    BookCreate
)
from models import (
    DBAuthor,
    DBBook
)


def get_author_by_id(db: Session, author_id: int):
    return db.execute(
        select(DBAuthor).where(DBAuthor.id == author_id)
    ).scalar_one_or_none()


def get_author_by_name(db: Session, author_name: str):
    return db.execute(
        select(DBAuthor).where(DBAuthor.name == author_name)
    ).scalar_one_or_none()


def get_all_authors(db: Session, skip: int = 0, limit: int = 10):
    return db.execute(
        select(DBAuthor).offset(skip).limit(limit)
    ).scalars().all()


def create_author(db: Session, author: AuthorCreate):
    db_author = DBAuthor(name=author.name, bio=author.bio)
    db.add(db_author)
    db.commit()
    db.refresh(db_author)

    return db_author


def get_book_by_title(db: Session, book_title: str):
    return db.execute(
        select(DBBook).where(DBBook.title == book_title)
    ).scalar_one_or_none()


def get_all_books(
        db: Session,
        author_id: Optional[int] = None,
        skip: int = 0,
        limit: int = 10
):
    stmt = select(DBBook)

    if author_id:
        stmt = stmt.where(DBBook.author_id == author_id)

    return db.execute(
        stmt.offset(skip).limit(limit)
    ).scalars().all()


def create_book(db: Session, book: BookCreate, author_id: int):
    db_book = DBBook(
        title=book.title,
        summary=book.summary,
        publication_date=book.publication_date,
        author_id=author_id
    )
    db.add(db_book)
    db.commit()
    db.refresh(db_book)

    return db_book
