from sqlalchemy import select
from sqlalchemy.orm import Session, joinedload

import models
import schemas


def get_all_authors(
    db: Session, skip: int = 0, limit: int = 10
) -> list[models.Author]:
    return list(
        db.scalars(
            select(models.Author)
            .order_by(models.Author.id)
            .offset(skip)
            .limit(limit)
        ).all()
    )


def get_author_by_id(db: Session, author_id: int) -> models.Author | None:
    return db.get(models.Author, author_id)


def get_books(
    db: Session, skip: int = 0, limit: int = 10, author_id: int | None = None
) -> list[models.Book]:
    stmt = select(models.Book).order_by(models.Book.id)
    if author_id is not None:
        stmt = stmt.where(models.Book.author_id == author_id)
    stmt = stmt.offset(skip).limit(limit)
    return list(db.scalars(stmt.options(joinedload(models.Book.author))).all())


def create_author(db: Session, author: schemas.AuthorCreate) -> models.Author:
    db_author = models.Author(name=author.name, bio=author.bio)
    db.add(db_author)
    db.commit()
    db.refresh(db_author)

    return db_author


def create_book(db: Session, book: schemas.BookCreate) -> models.Book:
    db_book = models.Book(
        title=book.title,
        summary=book.summary,
        publication_date=book.publication_date,
        author_id=book.author_id,
    )
    db.add(db_book)
    db.commit()
    db.refresh(db_book)

    return db_book


def get_author_by_name(db: Session, name: str) -> models.Author | None:
    return db.scalars(
        select(models.Author).where(models.Author.name == name)
    ).first()
