from sqlalchemy import select
from sqlalchemy.orm import Session

from db import models
import schemas


def get_all_books(
        db: Session,
        author_id: int | None = None,
        skip: int = 0,
        limit: int = 10,
):
    queryset = select(models.DBBook)

    if author_id is not None:
        queryset = queryset.where(models.DBBook.author_id == author_id)

    queryset = queryset.offset(skip).limit(limit)

    return db.scalars(queryset).all()


def get_one_book(
        db: Session,
        book_id: int,
):
    return db.scalar(
        select(models.DBBook).where(models.DBBook.id == book_id)
    )


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


def get_all_authors(
        db: Session,
        skip: int = 0,
        limit: int = 10,
):
    queryset = select(models.DBAuthor).offset(skip).limit(limit)
    return db.scalars(queryset).all()


def get_author_by_name(db: Session, name: str):
    result = db.execute(
        select(models.DBAuthor).where(models.DBAuthor.name == name))
    return result.scalar_one_or_none()



def get_one_author(
        db: Session,
        author_id: int,
):
    return db.scalar(
        select(models.DBAuthor).where(models.DBAuthor.id == author_id)
    )


def create_author(db: Session, author: schemas.AuthorCreate):
    db_author = models.DBAuthor(
        name=author.name,
        bio=author.bio
    )
    db.add(db_author)
    db.commit()
    db.refresh(db_author)
    return db_author
