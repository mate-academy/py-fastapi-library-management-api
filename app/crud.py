from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db import models
from app.schemas import BookCreateSchema, AuthorCreateSchema


# Author
def check_author_by_name_in_db(db: Session, author_name: str):
    return db.query(models.DBAuthor).filter_by(name=author_name).first()


def create_author(db: Session, author: AuthorCreateSchema) -> models.DBAuthor:
    db_author = models.DBAuthor(
        name=author.name,
        bio=author.bio
    )
    db.add(db_author)
    db.commit()
    db.refresh(db_author)

    return db_author


def get_all_authors(db: Session, skip: int, limit: int):
    stmt = select(models.DBAuthor).offset(skip).limit(limit)
    result = db.execute(stmt)
    return result.scalars().all()


def get_author_by_id(db: Session, author_id: int):
    return (
        db
        .query(models.DBAuthor)
        .filter(models.DBAuthor.id == author_id)
        .one_or_none()
    )


# Book
def get_all_books(db: Session, author_id: int, skip: int, limit: int):
    stmt = select(models.DBBook)
    if author_id:
        stmt = stmt.where(models.DBBook.author_id == author_id)

    stmt = stmt.offset(skip).limit(limit)

    result = db.execute(stmt)
    return result.scalars().all()


def create_book(db: Session, book: BookCreateSchema) -> models.DBBook:
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
