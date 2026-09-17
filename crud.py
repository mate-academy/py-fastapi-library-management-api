from sqlalchemy.orm import Session
from sqlalchemy import select

import models
import schemas


def create_new_author(db: Session, author_data: schemas.AuthorCreate):
    author = models.Author(
        name=author_data.name,
        bio=author_data.bio,
    )

    db.add(author)
    db.commit()
    db.refresh(author)

    return author


def search_by_name(db: Session, name: str):
    return db.scalar(select(models.Author).where(models.Author.name == name))


def search_author_by_id(db: Session, pk: int):
    return db.scalar(select(models.Author).where(models.Author.id == pk))


def create_book(
    db: Session,
    book: schemas.BookCreate,
):
    author = search_author_by_id(db, book.author_id)

    if author is None:
        return None

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


def get_authors(
    db: Session,
    skip: int = 0,
    limit: int = 10,
):
    return db.scalars(
        select(models.Author)
        .offset(skip)
        .limit(limit)
    ).all()


def get_books(
    db: Session,
    skip: int = 0,
    limit: int = 10,
    author_id: int | None = None,
):
    query = select(models.Book)

    if author_id is not None:
        query = query.where(models.Book.author_id == author_id)

    query = query.offset(skip).limit(limit)

    return db.scalars(query).all()
