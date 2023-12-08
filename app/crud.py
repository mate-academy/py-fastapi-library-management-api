from datetime import date

from sqlalchemy.orm import Session

from db import DBAuthor, DBBook

from .schemas import AuthorCreate, BookCreate


def get_authors(
    db: Session, skip: int = 0, limit: int = 100
) -> list[DBAuthor]:
    return db.query(DBAuthor).offset(skip).limit(limit).all()


def get_author_by_id(db: Session, author_id: int) -> DBAuthor | None:
    return db.query(DBAuthor).filter(DBAuthor.id == author_id).first()


def create_author(db: Session, author: AuthorCreate) -> DBAuthor:
    db_author = DBAuthor(**author.model_dump())
    db.add(db_author)
    db.commit()
    db.refresh(db_author)
    return db_author


def get_books(
    db: Session,
    skip: int,
    limit: int,
    title: str | None = None,
    summary: str | None = None,
    publication_date: date | None = None,
) -> list[DBBook]:
    queryset = db.query(DBBook)

    if title is not None:
        queryset = queryset.filter(DBBook.title == title)

    if summary is not None:
        queryset = queryset.filter(DBBook.summary == summary)

    if publication_date is not None:
        queryset = queryset.filter(DBBook.publication_date == publication_date)

    return queryset.offset(skip).limit(limit).all()


def get_book_by_id(db: Session, author_id: int) -> DBBook | None:
    return db.query(DBBook).filter(DBBook.author_id == author_id).first()


def create_book(db: Session, book: BookCreate) -> DBBook:
    db_book = DBBook(**book.model_dump())
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book
