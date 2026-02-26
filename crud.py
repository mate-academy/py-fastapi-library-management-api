from typing import Sequence

from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from models import DBAuthor, DBBook
from schemas import (
    AuthorBaseCreate,
    BookBaseCreate,
)


def create_author(
        db: Session,
        new_author: AuthorBaseCreate
) -> DBAuthor:
    db_author = DBAuthor(
        name=new_author.name,
        bio=new_author.bio,
    )

    db.add(db_author)
    db.commit()
    db.refresh(db_author)

    return db_author


def get_authors_with_pagination(
        db: Session,
        skip: int = 0,
        limit: int = 10,
) -> Sequence[DBAuthor]:
    return db.scalars(
        select(DBAuthor)
        .offset(skip)
        .limit(limit)
    ).all()


def get_author_by_id_or_404(
        db: Session,
        author_id: int
) -> DBAuthor:
    author = db.scalar(
        select(DBAuthor)
        .where(DBAuthor.id == author_id)
    )
    if not author:
        raise HTTPException(
            404,
            (
                f"Author with "
                f"(id: {author_id}) not found"
            )
        )
    return author


def get_author_by_name(
        db: Session,
        author_name: str
) -> DBAuthor:
    return db.scalar(
        select(DBAuthor)
        .where(DBAuthor.name == author_name)
    )


def create_book(
        db: Session,
        new_book: BookBaseCreate,
        author_id: int
) -> DBBook:
    db_book = DBBook(
        title=new_book.title,
        summary=new_book.summary,
        publication_date=new_book.publication_date,
        author_id=author_id
    )

    db.add(db_book)
    db.commit()
    db.refresh(db_book)

    return db_book


def get_books_with_pagination(
        db: Session,
        skip: int = 0,
        limit: int = 10,
) -> Sequence[DBBook]:
    return db.scalars(
        select(DBBook)
        .offset(skip)
        .limit(limit)
    ).all()


def filter_books_by_author_id(
        db: Session,
        author_id: int
) -> Sequence[DBBook]:
    return db.scalars(
        select(DBBook)
        .where(
            DBBook.author_id == author_id
        )
    ).all()
