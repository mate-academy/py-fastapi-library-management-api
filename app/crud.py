from sqlalchemy import select
from sqlalchemy.orm import Session

from app import schemas, models


def get_all_authors(db: Session, skip: int = 0, limit: int = 10) -> list[models.Author]:
    return db.scalars(
        select(models.Author).order_by(models.Author.id).offset(skip).limit(limit)
    ).all()


def get_author_by_id(db: Session, author_id: int) -> models.Author | None:
    return db.scalar(select(models.Author).where(models.Author.id == author_id))


def get_author_by_name(db: Session, author_name: str) -> models.Author | None:
    return db.scalar(select(models.Author).where(models.Author.name == author_name))


def create_author(db: Session, author: schemas.AuthorCreate) -> models.Author:
    db_author = models.Author(name=author.name, bio=author.bio)

    db.add(db_author)
    db.commit()
    db.refresh(db_author)

    return db_author


def get_all_books(
    db: Session,
    author_id: int | None = None,
    skip: int = 0,
    limit: int = 10,
) -> list[models.Book]:
    stmt = select(models.Book)

    if author_id:
        stmt = stmt.where(models.Book.author_id == author_id)

    return db.scalars(stmt.order_by(models.Book.id).offset(skip).limit(limit)).all()


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
