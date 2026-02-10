from fastapi import HTTPException
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
    new_author = Author(
        name=author.name,
        bio=author.bio
    )
    db.add(new_author)
    db.commit()
    db.refresh(new_author)
    return new_author


def read_authors_list(
    db: Session,
    skip: int = 0,
    limit: int = 100
) -> list[Author]:
    queryset = select(Author).offset(skip).limit(limit)
    return db.scalars(queryset).all()


def read_author_detail(db: Session, author_id: int) -> Author:
    author = db.get(Author, author_id)

    if author is None:
        raise HTTPException(status_code=404, detail="Not found")

    return author


def update_author(
    db: Session,
    author_id: int,
    author: AuthorCreateUpdateSchema
) -> Author:
    author_init = db.get(Author, author_id)

    if author_init is None:
        raise HTTPException(status_code=404, detail="Not found")

    author_init.name = author.name
    author_init.bio = author.bio
    db.commit()
    db.refresh(author_init)
    return author_init


def delete_author(db: Session, author_id: int) -> None:
    author = db.get(Author, author_id)

    if author is None:
        raise HTTPException(status_code=404, detail="Not found")

    db.delete(author)
    db.commit()


def create_book(db: Session, book: BookCreateUpdateSchema) -> Book:
    author = db.get(Author, book.author_id)

    if author is None:
        raise HTTPException(status_code=404, detail="Author not found")

    new_book = Book(
        title=book.title,
        summary=book.summary,
        publication_date=book.publication_date,
        author_id=book.author_id
    )
    db.add(new_book)
    db.commit()
    db.refresh(new_book)
    return new_book


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
    book = db.get(Book, book_id)

    if book is None:
        raise HTTPException(status_code=404, detail="Not found")

    return book


def update_book(
    db: Session,
    book_id: int,
    book: BookCreateUpdateSchema
) -> Book:
    book_init = db.get(Book, book_id)

    if book_init is None:
        raise HTTPException(status_code=404, detail="Not found")

    book_init.title = book.title
    book_init.summary = book.summary
    book_init.publication_date = book.publication_date

    author = db.get(Author, book.author_id)

    if author is None:
        raise HTTPException(status_code=404, detail="Author not found")

    book_init.author_id = book.author_id
    db.commit()
    db.refresh(book_init)
    return book_init


def delete_book(db: Session, book_id: int) -> None:
    book = db.get(Book, book_id)

    if book is None:
        raise HTTPException(status_code=404, detail="Not found")

    db.delete(book)
    db.commit()
