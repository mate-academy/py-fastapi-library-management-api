from sqlalchemy import select
from sqlalchemy.orm import Session

import schemas
from db import models
from db.models import DBBook


def get_all_authors(
        db: Session,
        skip: int = 0,
        limit: int = 10
) -> list[models.DBAuthor]:
    query =select(models.DBAuthor).offset(skip).limit(limit)
    return db.scalars(query).all()

def get_author_by_id(
        db: Session, author_id:int
) -> models.DBAuthor | None:
    return db.scalar(
        select(models.DBAuthor).where(models.DBAuthor.id == author_id)
    )


def get_author_by_name(db: Session, name: str) -> models.DBAuthor | None:
    return db.scalar(select(models.DBAuthor).where(models.DBAuthor.name == name))


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


def get_book_list(
        db: Session,
        skip: int = 0,
        limit: int = 10
) -> list[models.DBBook]:
    query = select(models.DBBook).offset(skip).limit(limit)
    return db.scalars(query).all()


def get_book_by_author_id(
        db: Session,
        author_id: int
) -> list[models.DBBook]:
    return db.scalars(
        select(models.DBBook).where(models.DBBook.author_id == author_id)
    ).all()


def create_book(
        db: Session,
        book: schemas.BookCreate
) -> models.DBBook:
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