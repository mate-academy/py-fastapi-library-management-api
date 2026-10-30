from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload

import models
import schemas


# author
def get_author_by_name(db: Session, name: str):
    return db.scalar(select(models.Author).where(models.Author.name == name))


def create_author(db: Session, author: schemas.AuthorCreate):
    db_author = models.Author(
        name=author.name,
        bio=author.bio,
    )
    db.add(db_author)
    db.commit()
    db.refresh(db_author)
    return db_author


def get_all_authors(db: Session, skip: int = 0, limit: int = 10):
    query = (
        select(models.Author)
        .options(selectinload(models.Author.books))
        .order_by(models.Author.id)
        .offset(skip)
        .limit(limit)
    )
    return db.scalars(query).all()


def get_author(db: Session, author_id: int):
    return db.get(models.Author, author_id)


# book
def get_books(
    db: Session,
    author_id: int | None = None,
    skip: int = 0,
    limit: int = 10,
):
    query = select(models.Book).order_by(models.Book.id)

    if author_id is not None:
        query = query.where(models.Book.author_id == author_id)

    return db.scalars(query.offset(skip).limit(limit)).all()


def create_book(db: Session, book: schemas.BookCreate):
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
