from sqlalchemy import select
from sqlalchemy.orm import Session

import models
from schemas import AuthorCreate, BookCreate


def create_author(db: Session, author: AuthorCreate):
    db_author = models.DBAuthor(
        name=author.name,
        bio=author.bio
    )
    db.add(db_author)
    db.commit()
    db.refresh(db_author)

    return db_author


def get_authors(db: Session, skip: int = 0, limit: int = 10):
    return db.execute(
        select(models.DBAuthor).offset(skip).limit(limit)
    ).scalars().all()


def get_author(db: Session, author_id: int):
    return db.scalar(
        select(models.DBAuthor).where(models.DBAuthor.id == author_id)
    )


def create_book(db: Session, book: BookCreate, author_id: int):
    db_book = models.DBBook(
        title=book.title,
        summary=book.summary,
        publication_date=book.publication_date,
        author_id=author_id
    )
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book


def get_books(
        db: Session,
        skip: int = 0,
        limit: int = 10,
        author_id: int | None = None
):
    queryset = select(models.DBBook)
    if author_id is not None:
        queryset = queryset.where(models.DBBook.author_id == author_id)

    queryset = queryset.offset(skip).limit(limit)

    return db.execute(queryset).scalars().all()
