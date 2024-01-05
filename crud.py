from datetime import date

from sqlalchemy.orm import Session

from db import models
import schemas


def get_all_authors(
        db: Session,
        limit: int = 10,
        skip: int = 0,
        book: str | None = None
):
    queryset = db.query(models.DBAuthor)

    if book:
        queryset = queryset.filter(models.DBAuthor.books.has(name=book))

    queryset = queryset.offset(skip).limit(limit)

    return queryset.all()


def get_author_by_name(db: Session, name: str):
    return (
        db.query(models.DBAuthor).filter(models.DBAuthor.name == name).first()
    )


def get_author_by_id(db: Session, author_id: int):
    return db.query(models.DBAuthor).filter(models.DBAuthor.id == author_id).first()


def create_author(db: Session, author: schemas.AuthorCreate):
    db_author = models.DBAuthor(
        name=author.name,
        bio=author.bio
    )
    db.add(db_author)
    db.commit()
    db.refresh(db_author)
    return db_author


def get_book_list(
    db: Session,
    skip: int = 0,
    limit: int = 10,
    publication_date: date | None = None,
    author: str | None = None
):

    queryset = db.query(models.DBBook)

    if author:
        queryset = queryset.filter(
            models.DBBook.author.has(name=author)
        )

    if publication_date:
        queryset = queryset.filter(
            models.DBBook.publication_date == publication_date
        )

    queryset = queryset.offset(skip).limit(limit)

    return queryset.all()


def get_book(db: Session, book_id: int):
    return db.query(models.DBBook).filter(models.DBBook.id == book_id).first()


def create_book(db: Session, book: schemas.BookCreate):
    db_book = models.DBBook(
        title=book.title,
        summary=book.summary,
        publication_date=book.publication_date,
        author_id=book.author_id
    )
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book

