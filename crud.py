from sqlalchemy.orm import Session
from typing import Type

from models import Author, Book
from schemas import AuthorCreate, BookCreate


def create_author(db: Session, author: AuthorCreate) -> Author:
    db_author = Author(name=author.name, bio=author.bio)
    db.add(db_author)
    db.commit()
    db.refresh(db_author)
    return db_author


def get_authors(db: Session, skip: int = 0, limit: int = 10) -> list[Type[Author]]:
    return db.query(Author).offset(skip).limit(limit).all()


def get_author_by_id(db: Session, author_id: int) -> Author | None:
    return db.query(Author).filter(Author.id == author_id).first()


def create_book(db: Session, book: BookCreate, author_id: int) -> Book:
    db_book = Book(
        title=book.title,
        summary=book.summary,
        publication_date=book.publication_date,
        author_id=author_id
    )
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book


def get_books(db: Session, skip: int = 0, limit: int = 10) -> list[Type[Book]]:
    return db.query(Book).offset(skip).limit(limit).all()


def get_books_by_author(db: Session, author_id: int) -> list[Type[Book]]:
    return db.query(Book).filter(Book.author_id == author_id).all()
