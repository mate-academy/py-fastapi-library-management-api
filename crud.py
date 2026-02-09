from sqlalchemy import select
from sqlalchemy.orm import Session

from models import Author, Book
from schemas import (
    AuthorCreateUpdateSchema,
    BookCreateUpdateSchema
)


def create_author(
    db: Session,
    author: AuthorCreateUpdateSchema
) -> Author:
    author = Author(
        name=author.name,
        bio=author.bio
    )
    db.add(author)
    db.commit()
    db.refresh(author)
    return author


def read_authors_list(
    db: Session,
    skip: int = 0,
    limit: int = 100
) -> list[Author]:
    queryset = select(Author).offset(skip).limit(limit)
    return db.scalars(queryset).all()


def read_author_detail(db: Session, author_id: int) -> Author:
    return db.get(Author, author_id)


def update_author(
    db: Session,
    author_id: int,
    author: AuthorCreateUpdateSchema
) -> Author:
    author_init = db.get(Author, author_id)
    author_init.name = author.name
    author_init.bio = author.bio
    db.commit()
    db.refresh(author_init)
    return author_init


def delete_author(db: Session, author_id: int) -> None:
    author = db.get(Author, author_id)
    db.delete(author)
    db.commit()


def create_book(db: Session, book: BookCreateUpdateSchema) -> Book:
    book = Book(
        title=book.title,
        summary=book.summary,
        publication_date=book.publication_date,
        author_id=book.author_id
    )
    db.add(book)
    db.commit()
    db.refresh(book)
    return book


def read_books_list(
    db: Session, author_id: int | None = None,
    skip: int = 0, limit: int = 100
) -> list[Book]:
    queryset = select(Book)

    if author_id is not None:
        queryset = queryset.where(Book.author_id == author_id)

    queryset = queryset.offset(skip).limit(limit)

    return db.scalars(queryset).all()


def read_book_detail(db: Session, book_id: int) -> Book:
    return db.get(Book, book_id)


def update_book(
    db: Session,
    book_id: int,
    book: BookCreateUpdateSchema
) -> Book:
    book_init = db.get(Book, book_id)
    book_init.title = book.title
    book_init.summary = book.summary
    book_init.publication_date = book.publication_date
    book_init.author_id = book.author_id
    db.commit()
    db.refresh(book_init)
    return book_init


def delete_book(db: Session, book_id: int) -> None:
    book = db.get(Book, book_id)
    db.delete(book)
    db.commit()
