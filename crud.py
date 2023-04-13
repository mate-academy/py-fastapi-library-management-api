from typing import Optional

from sqlalchemy.orm import Session
from models import Author, Book
import schemas


def create_author(db: Session, author: schemas.AuthorCreate) -> Author:
    new_author = Author(
        name=author.name,
        bio=author.bio
    )
    db.add(new_author)
    db.commit()
    db.refresh(new_author)
    return new_author


def get_authors_list(
        db: Session,
        skip: int = 0,
        limit: int = 100
) -> list[Author]:
    return db.query(Author).offset(skip).limit(limit).all()


def get_author(db: Session, author_id: int) -> Optional[Author]:
    return db.query(Author).filter(Author.id == author_id).first()


def create_book(
        db: Session,
        book: schemas.BookCreate,
        author_id: int
) -> Book:
    new_book = Book(**book.dict(), author_id=author_id)
    db.add(new_book)
    db.commit()
    db.refresh(new_book)
    return new_book


def get_books_list(
        db: Session,
        skip: int = 0,
        limit: int = 100
) -> list[Book]:
    return db.query(Book).offset(skip).limit(limit).all()


def get_books_by_author(
        db: Session,
        author_id: int
) -> Book:
    return db.query(Book).filter(Book.author_id == author_id).all()
