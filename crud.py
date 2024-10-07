from typing import Optional, Type

from sqlalchemy.orm import Session
from db.models import Author, Book
import schemas


def get_author(db: Session, author_id: int) -> Optional[Author]:
    return db.query(Author).filter(Author.id == author_id).first()


def get_authors(db: Session, skip: int = 0, limit: int = 10) -> list[Type[Author]]:
    return db.query(Author).offset(skip).limit(limit).all()


def create_author(db: Session,
                  author: schemas.AuthorCreate) -> Optional[Author]:
    db_author = Author(**author.dict())
    db.add(db_author)
    db.commit()
    db.refresh(db_author)
    return db_author


def create_book(db: Session,
                book: schemas.BookCreate) -> Optional[Book]:
    db_book = Book(**book.dict())
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book


def get_books(db: Session,
              skip: int = 0,
              limit: int = 10,
              author_id: Optional[int] = None) -> list[Type[Book]]:
    query = db.query(Book)
    if author_id:
        query = query.filter(Book.author_id == author_id)
    return query.offset(skip).limit(limit).all()
