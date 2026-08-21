from sqlalchemy import select
from sqlalchemy.orm import Session

from db import models
import schemas


class AuthorNotFoundError(Exception):
    """Author with given id does not exist."""


class AuthorNameAlreadyExistsError(Exception):
    """Another author with this name already exists."""


class BookNotFoundError(Exception):
    """Book with given id does not exist."""


def get_all_authors(
        db: Session,
        skip: int = 0,
        limit: int = 10,
):
    return db.scalars(
        select(models.Author)
        .order_by(models.Author.id)
        .offset(skip)
        .limit(limit)
    ).all()


def get_author_by_name(db: Session, name: str):
    return db.scalar(select(models.Author).where(models.Author.name == name))


def get_author(db: Session, author_id: int):
    return db.scalar(
        select(models.Author).where(models.Author.id == author_id)
    )


def create_author(db: Session, author: schemas.AuthorCreate):
    if get_author_by_name(db, author.name):
        raise AuthorNameAlreadyExistsError

    db_author = models.Author(
        name=author.name,
        bio=author.bio,
    )
    db.add(db_author)
    db.commit()
    db.refresh(db_author)

    return db_author


def update_author(
    db: Session,
    author_id: int,
    author: schemas.AuthorCreate,
):
    db_author = get_author(db, author_id)
    if db_author is None:
        raise AuthorNotFoundError

    existing_author = get_author_by_name(db, author.name)
    if existing_author and existing_author.id != author_id:
        raise AuthorNameAlreadyExistsError

    db_author.name = author.name
    db_author.bio = author.bio

    db.commit()
    db.refresh(db_author)

    return db_author


def delete_author(db: Session, author_id: int) -> None:
    db_author = get_author(db, author_id)
    if db_author is None:
        raise AuthorNotFoundError

    db.delete(db_author)
    db.commit()


def get_all_books(
        db: Session,
        author_id: int | None = None,
        skip: int = 0,
        limit: int = 10,
):
    queryset = select(models.Book)
    if author_id is not None:
        queryset = queryset.join(models.Author).where(
            models.Book.author_id == author_id
        )
    return db.scalars(
        queryset
        .order_by(models.Book.id)
        .offset(skip)
        .limit(limit)
    ).all()


def get_book(db: Session, book_id: int):
    return db.scalar(
        select(models.Book).where(models.Book.id == book_id)
    )


def create_book(db: Session, book: schemas.BookCreate):
    db_book = models.Book(
        title=book.title,
        summary=book.summary,
        publication_date=book.publication_date,
        author_id=book.author_id,
    )
    db.add(db_book)
    db.commit()
    db.refresh(db_book)

    return db_book


def update_book(
        db: Session,
        book_id: int,
        book: schemas.BookCreate,
):
    db_book = get_book(db, book_id)

    if db_book is None:
        raise BookNotFoundError

    db_book.title = book.title
    db_book.summary = book.summary
    db_book.publication_date = book.publication_date
    db_book.author_id = book.author_id

    db.commit()
    db.refresh(db_book)

    return db_book


def delete_book(db: Session, book_id: int) -> None:
    db_book = get_book(db, book_id)
    if db_book is None:
        raise BookNotFoundError

    db.delete(db_book)
    db.commit()
