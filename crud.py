from __future__ import annotations

from datetime import date
from typing import List, Optional

from sqlalchemy.orm import Session

from models import Author, Book
from schemas import AuthorCreate, BookCreate


# --------- Authors ---------
def create_author(db: Session, author_in: AuthorCreate) -> Author:
    author = Author(name=author_in.name, bio=author_in.bio)
    db.add(author)
    db.commit()
    db.refresh(author)
    return author


def get_authors(db: Session, skip: int = 0, limit: int = 10) -> List[Author]:
    return db.query(Author).offset(skip).limit(limit).all()


def get_author_by_id(db: Session, author_id: int) -> Optional[Author]:
    return db.query(Author).filter(Author.id == author_id).first()


def get_author_by_name(db: Session, name: str) -> Optional[Author]:
    return db.query(Author).filter(Author.name == name).first()


# --------- Books ---------
def create_book_for_author(db: Session, author_id: int, book_in: BookCreate) -> Book:
    book = Book(
        title=book_in.title,
        summary=book_in.summary,
        publication_date=book_in.publication_date,
        author_id=author_id,
    )
    db.add(book)
    db.commit()
    db.refresh(book)
    return book


def get_books(
    db: Session,
    skip: int = 0,
    limit: int = 10,
    author_id: Optional[int] = None,
) -> List[Book]:
    q = db.query(Book)
    if author_id is not None:
        q = q.filter(Book.author_id == author_id)
    return q.offset(skip).limit(limit).all()
