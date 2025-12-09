from sqlalchemy import select
from sqlalchemy.orm import Session
import schemas
from db import models


def get_all_authors(
        skip: int,
        limit: int,
        db: Session) -> list[models.DBAuthor]:
    stmt = select(models.DBAuthor).offset(skip).limit(limit)
    result = db.scalars(stmt).all()
    return result


def get_author_by_id(
        db: Session, author_id: int
) -> models.DBAuthor | None:
    return db.scalar(
        select(models.DBAuthor)
        .where(models.DBAuthor.id == author_id)
    )


def get_author_by_name(
        db: Session,
        name: str
) -> models.DBAuthor | None:
    return db.scalar(
        select(models.DBAuthor).where(models.DBAuthor.name == name)
    )


def create_author(
        db: Session,
        author: schemas.AuthorCreate
) -> models.DBAuthor:
    db_author = models.DBAuthor(
        name=author.name,
        bio=author.bio
    )
    db.add(db_author)
    db.commit()
    db.refresh(db_author)
    return db_author


def get_books_list(
        skip: int,
        limit: int,
        db: Session,
        author_id: int | None = None
) -> list[models.DBBook]:
    stmt = select(models.DBBook).offset(skip).limit(limit)
    if author_id:
        stmt = stmt.where(models.DBBook.author_id == author_id)
    return db.scalars(stmt).all()


def get_book_by_title(
        db: Session,
        title: str
) -> models.DBBook | None:
    return db.scalar(
        select(models.DBBook).where(models.DBBook.title == title)
    )


def create_book(
        db: Session,
        book: schemas.BookCreate
) -> models.DBBook:
    db_book = models.DBBook(
        author_id=book.author_id,
        title=book.title,
        summary=book.summary,
        publication_date=book.publication_date
    )
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book
