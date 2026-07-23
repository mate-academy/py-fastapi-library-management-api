from sqlalchemy import select
from sqlalchemy.orm import Session

import schemas
from models import DBAuthor, DBBook


def create_author(
    db: Session,
    author: schemas.AuthorCreate,
):
    db_author = DBAuthor(
        name=author.name,
        bio=author.bio,
    )
    db.add(db_author)
    db.commit()
    db.refresh(db_author)
    return db_author


def get_list_authors(db: Session, skip: int = 0, limit: int = 5):
    queryset = select(DBAuthor).offset(skip).limit(limit)
    return db.scalars(queryset).all()


def get_author_by_id(db: Session, author_id: int):
    return db.scalar(select(DBAuthor).where(DBAuthor.id == author_id))


def create_book_for_author(
    db: Session,
    book: schemas.BookCreate,
):
    db_book = DBBook(
        title=book.title,
        summary=book.summary,
        publication_date=book.publication_date,
        author_id=book.author_id,
    )
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book


def get_books_list(
    db: Session,
    skip: int = 0,
    limit: int = 5,
    author_id: int | None = None,
):
    queryset = select(DBBook).offset(skip).limit(limit)

    if author_id is not None:
        queryset = queryset.where(DBBook.author_id == author_id)

    return db.scalars(queryset).all()
