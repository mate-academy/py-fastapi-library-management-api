from sqlalchemy import select
from sqlalchemy.orm import Session

from models import Author, Book
from schemas import AuthorCreate, BookCreate


def get_all_authors(
        database: Session,
        skip: int = 0,
        limit: int = 100
):
    return database.scalars(
        select(Author).offset(skip).limit(limit)
    ).all()


def get_author_by_id(database: Session, author_id: int):
    return database.scalar(
        select(Author).where(Author.id == author_id)
    )


def get_author_by_name(database: Session, name: str):
    return database.scalar(
        select(Author).where(Author.name == name)
    )


def create_author(database: Session, author: AuthorCreate):
    database_author = Author(
        name=author.name,
        bio=author.bio,
    )

    database.add(database_author)
    database.commit()
    database.refresh(database_author)

    return database_author


def get_all_books(
        database: Session,
        skip: int = 0,
        limit: int = 100,
        author_id: int | None = None
):
    queryset = select(Book)

    if author_id is not None:
        queryset = queryset.where(Book.author_id == author_id)

    return database.scalars(queryset.offset(skip).limit(limit)).all()


def get_book_by_id(database: Session, book_id: int):
    return database.scalar(
        select(Book).where(Book.id == book_id)
    )


def create_book(database: Session, book: BookCreate, author_id: int):
    database_book = Book(
        title=book.title,
        summary=book.summary,
        publication_date=book.publication_date,
        author_id=author_id,
    )

    database.add(database_book)
    database.commit()
    database.refresh(database_book)

    return database_book
