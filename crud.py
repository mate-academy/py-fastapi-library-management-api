from datetime import date
from typing import Sequence

from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from models import Author, Book
from schemas import AuthorCreate, AuthorUpdate, BookCreate, BookUpdate
from validation import validate_author_with_name_exists


def get_all_authors(
        db: Session,
        skip: int = 0,
        limit: int = 10
) -> Sequence[Author]:
    return db.scalars(select(Author).offset(skip).limit(limit)).all()


def get_author_by_name(db: Session, name: str) -> Author:
    return db.scalar(select(Author).where(Author.name == name))


def get_author_by_id(db: Session, author_id: int) -> Author:
    return db.scalar(select(Author).where(Author.id == author_id))


def create_author(db: Session, author: AuthorCreate) -> Author:
    validate_author_with_name_exists(db=db, author_name=author.name)
    db_author = Author(**author.model_dump())

    db.add(db_author)
    db.commit()
    db.refresh(db_author)

    return db_author


def update_author(
        db: Session,
        author_id: int,
        data: AuthorUpdate
) -> Author:

    validate_author_with_name_exists(
        db=db, author_name=data.name, author_id=author_id
    )

    author = db.get(Author, author_id)

    if not author:
        raise HTTPException(status_code=404, detail="Author not found")

    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(author, field, value)

    db.commit()
    db.refresh(author)
    return author


def delete_author(db: Session, author_id: int) -> Author:
    author = db.get(Author, author_id)
    if not author:
        raise HTTPException(status_code=404, detail="Author not found")
    db.delete(author)
    db.commit()
    return author


def get_books_list(
        db: Session,
        title: str | None = None,
        publication_date: date | None = None,
        author: int | None = None,
        skip: int = 0,
        limit: int = 10
) -> Sequence[Book]:

    queryset = db.query(Book)

    if title:
        queryset = queryset.where(Book.title == title)
    if publication_date:
        queryset = queryset.where(
            Book.publication_date == publication_date
        )
    if author:
        queryset = queryset.join(Author).where(
            Author.id == author
        )

    return db.scalars(queryset.offset(skip).limit(limit)).all()


def get_book(db: Session, book_id: int) -> Book:
    return db.scalar(select(Book).where(Book.id == book_id))


def create_book(db: Session, book: BookCreate) -> Book:
    db_book = Book(**book.model_dump())
    if not db.get(Author, db_book.author_id):
        raise HTTPException(status_code=404, detail="Author not found")

    db.add(db_book)
    db.commit()
    db.refresh(db_book)

    return db_book


def update_book(db: Session, book_id: int, data: BookUpdate) -> Book:
    book = db.get(Book, book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(book, field, value)

    db.commit()
    db.refresh(book)
    return book


def delete_book(db: Session, book_id: int) -> Book:
    book = db.get(Book, book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    db.delete(book)
    db.commit()
    return book
