from sqlalchemy import select
from sqlalchemy.orm import Session

from db import models
from schemas import AuthorCreate, BookCreate


def get_all_authors(
        db: Session,
        author_id: int | None = None,
        skip: int = 0,
        limit: int = 100,
):
    queryset = select(models.DBAuthor)

    if id is not None:
        queryset = queryset.where(models.DBAuthor.author_id == author_id)

    return db.scalars(queryset.offset(skip).limit(limit)).all()


def get_author_by_name(db: Session, name: str):
    return (
        db.scalar(select(models.DBAuthor).where(models.DBAuthor.name == name))
    )

def create_author(db: Session, author: AuthorCreate):
    db_author = models.DBAuthor(
        name=author.name,
        bio=author.bio
    )
    db.add(db_author)
    db.commit()
    db.refresh(db_author)

    return db_author


def get_books_list(
        db: Session,
        author_id: int | None = None,
        skip: int = 0,
        limit: int = 100,
):
    queryset = select(models.DBBook)

    if author_id is not None:
        queryset = queryset.where(
            models.DBBook.author_id == author_id
        )

    return db.scalars(queryset.offset(skip).limit(limit)).all()

def create_book(db: Session, book: BookCreate):
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
