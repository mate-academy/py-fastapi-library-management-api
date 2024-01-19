from fastapi import Query
from sqlalchemy.orm import Session

import schemas
from db.models import DBAuthor, DBBook


def get_author_list(db: Session) -> Query:
    return db.query(DBAuthor).all()


def get_author(db: Session, author_id: int) -> Query:
    return db.query(DBAuthor).filter(DBAuthor.id == author_id).first()


def create_author(db: Session, author: schemas.AuthorCreate) -> DBAuthor:
    db_author = DBAuthor(
        name=author.name,
        bio=author.bio,
    )
    db.add(db_author)
    db.commit()
    db.refresh(db_author)

    return db_author


def get_book_list(db: Session, author_id: int | None = None) -> Query:
    queryset = db.query(DBBook)

    if author_id:
        queryset = queryset.filter(DBBook.author_id == author_id)

    return queryset.all()


def create_book_for_a_specific_author(
    db: Session, author_id: int, book: schemas.BookCreate
) -> DBBook:
    db_book = DBBook(
        title=book.title,
        summary=book.summary,
        publication_date=book.publication_date,
        author_id=author_id,
    )
    db.add(db_book)
    db.commit()
    db.refresh(db_book)

    return db_book
