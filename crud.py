from typing import List

from sqlalchemy.orm import Session

from models import Author, Book
from schemas import (AuthorBaseSchema,
                     AuthorCreateSchema,
                     BookBaseSchema,
                     BookCreateSchema,
                     BookSchema,
                     PaginatedBooksSchema,
                     PaginatedAuthorsSchema)


def create_author(db: Session, author: AuthorCreateSchema) -> Author:
    db_author = Author(name=author.name, bio=author.bio)
    db.add(db_author)
    db.commit()
    db.refresh(db_author)
    return db_author


def get_author(db: Session, author_id: int) -> Author:
    return db.query(Author).filter(Author.id == author_id).first()


def get_author_by_name(db: Session, name: str) -> Author:
    return db.query(Author).filter(Author.name == name).first()


def get_authors(db: Session, skip: int = 0, limit: int = 10) -> PaginatedAuthorsSchema:
    authors = db.query(Author).offset(skip).limit(limit).all()
    total = db.query(Author).count()
    return PaginatedAuthorsSchema(total=total, page=skip // limit + 1, per_page=limit, authors=authors)


def create_book(db: Session, book: BookCreateSchema) -> Book:
    db_book = Book(
        title=book.title,
        summary=book.summary,
        published_date=book.published_date,
        author_id=book.author_id
    )
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book


def get_book_by_title(db: Session, title: str) -> Book:
    return db.query(Book).filter(Book.title == title).first()


def get_books(db: Session, skip: int = 0, limit: int = 10) -> PaginatedBooksSchema:
    books = db.query(Book).offset(skip).limit(limit).all()
    total = db.query(Book).count()
    return PaginatedBooksSchema(total=total, page=skip // limit + 1, per_page=limit, books=books)


def get_books_by_author(db: Session, author_id: int, skip: int = 0, limit: int = 10) -> PaginatedBooksSchema:
    books = db.query(Book).filter(Book.author_id == author_id).offset(skip).limit(limit).all()
    total = db.query(Book).filter(Book.author_id == author_id).count()
    return PaginatedBooksSchema(total=total, page=skip // limit + 1, per_page=limit, books=books)