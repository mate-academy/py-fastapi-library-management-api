from typing import List, Optional

from sqlalchemy import select
from sqlalchemy.orm import Session

from models import Author, Book
import schemas


def get_all_authors(db: Session, skip: int = 0, limit: int = 10) -> List[Author]:
    return db.execute(select(Author).offset(skip).limit(limit)).scalars().all()


def create_author(db: Session, author: schemas.AuthorCreate) -> Author:
    db_author = Author(
        name=author.name,
        bio=author.bio
    )
    db.add(db_author)
    db.commit()
    db.refresh(db_author)

    return db_author


def get_author_by_id(db: Session, author_id: int) -> Optional[Author]:
    return db.execute(select(Author).filter_by(id=author_id)).scalar_one_or_none()


def get_all_books(
        db: Session,
        author_id: int = None,
        skip: int = 0,
        limit: int = 10
) -> List[Book]:
    query = select(Book)
    if author_id:
        query = query.filter(Book.author_id == author_id)
    return db.execute(query.offset(skip).limit(limit)).scalars().all()


def create_book(db: Session, book: schemas.BookCreate) -> Book:
    db_book = Book(
        title=book.title,
        author_id=book.author_id,
        summary=book.summary,
        publication_date=book.publication_date,
    )
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book
