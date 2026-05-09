from sqlalchemy import select
from sqlalchemy.orm import Session

import models
import schemas


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


def retrieve_author_by_id(
    db: Session,
    author_id: int
) -> models.DBAuthor:

    return db.get(models.DBAuthor, author_id)


def get_author_by_name(
    db: Session,
    name: str
) -> models.DBAuthor:
    stmt = select(models.DBAuthor).where(models.DBAuthor.name == name)

    return db.scalars(stmt).first()


def retrieve_authors(
    db: Session,
    skip: int = 0,
    limit: int = 100
) -> list[models.DBAuthor]:
    stmt = select(models.DBAuthor).offset(skip).limit(limit)

    return list(db.scalars(stmt).all())


def create_book(
    db: Session,
    book: schemas.BookCreate
) -> models.DBBook:

    db_book = models.DBBook(
        title=book.title,
        summary=book.summary,
        author_id=book.author_id,
        publication_date=book.publication_date
    )
    db.add(db_book)
    db.commit()
    db.refresh(db_book)

    return db_book


def retrieve_books(
    db: Session,
    skip: int = 0,
    limit: int = 100,
    author_id: int | None = None
) -> list[models.DBBook]:
    stmt = select(models.DBBook).offset(skip).limit(limit)
    if author_id:
        stmt = stmt.where(
            models.DBBook.author_id == author_id
        )

    return list(db.scalars(stmt).all())
