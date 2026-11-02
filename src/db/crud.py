from sqlalchemy import select
from sqlalchemy.orm import Session

from src.db.models import Author, Book
from src.db.schemas import AuthorCreate, BookCreate


def create_author(db: Session, author: AuthorCreate) -> Author:
    db_author = Author(**author.model_dump())
    db.add(db_author)
    db.commit()
    db.refresh(db_author)
    return db_author


def get_author_by_name(db: Session, author_name: str) -> Author | None:
    return db.scalar(select(Author).where(Author.name == author_name))


def get_author_by_id(db: Session, author_id: int) -> Author | None:
    return db.scalar(select(Author).where(Author.id == author_id))


def get_authors(db: Session, skip: int = 0, limit: int = 100) -> list[Author]:
    return list(db.scalars(select(Author).offset(skip).limit(limit)))


def create_book(db: Session, book: BookCreate, author_id: int) -> Book:
    db_book = Book(**book.model_dump(), author_id=author_id)
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book


def get_book(db: Session, book_id: int) -> Book | None:
    return db.get(Book, book_id)


def get_books(db: Session, author_id: int | None = None, skip: int = 0, limit: int = 100) -> list[Book]:
    queryset = select(Book)
    if author_id is not None:
        queryset = queryset.where(Book.author_id == author_id)
    return list(db.scalars(queryset.offset(skip).limit(limit)))
