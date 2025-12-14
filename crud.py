from sqlalchemy.orm import Session
from sqlalchemy import select

import models
import schemas


def get_author(db: Session, author_id: int) -> models.Author | None:
    return db.get(models.Author, author_id)


def get_author_by_name(db: Session, name: str) -> models.Author | None:
    stmt = select(models.Author).where(models.Author.name == name)
    return db.scalar(stmt)


def get_authors(db: Session, skip: int = 0, limit: int = 100) -> list[models.Author]:
    stmt = select(models.Author).offset(skip).limit(limit)
    return db.scalars(stmt).all()


def create_author(db: Session, author_in: schemas.AuthorCreate) -> models.Author:
    author = models.Author(name=author_in.name, bio=author_in.bio)
    db.add(author)
    db.commit()
    db.refresh(author)
    return author


def get_books(
    db: Session,
    skip: int = 0,
    limit: int = 100,
    author_id: int | None = None,
) -> list[models.Book]:
    stmt = select(models.Book)
    if author_id is not None:
        stmt = stmt.where(models.Book.author_id == author_id)
    stmt = stmt.offset(skip).limit(limit)
    return db.scalars(stmt).all()


def create_book_for_author(
    db: Session,
    author_id: int,
    book_in: schemas.BookCreate,
) -> models.Book:
    book = models.Book(
        title=book_in.title,
        summary=book_in.summary,
        publication_date=book_in.publication_date,
        author_id=author_id,
    )
    db.add(book)
    db.commit()
    db.refresh(book)
    return book
