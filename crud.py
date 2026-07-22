from typing import Sequence

from sqlalchemy import func, select
from sqlalchemy.orm import Session

import models
from schemas import AuthorCreateSchema, BookCreateSchema


def get_all_authors(
    session: Session, skip: int = 0, limit: int = 10
) -> Sequence[models.Author]:
    stmt = select(models.Author).order_by(models.Author.id).offset(skip).limit(limit)
    return session.execute(stmt).scalars().all()


def get_author_by_id(session: Session, author_id: int) -> type[models.Author] | None:
    return session.get(models.Author, author_id)


def create_author(session: Session, data: AuthorCreateSchema) -> models.Author:
    author = models.Author(**data.model_dump())
    session.add(author)
    session.commit()
    session.refresh(author)
    return author


def count_authors(session: Session) -> int:
    stmt = select(func.count()).select_from(models.Author)
    return session.execute(stmt).scalar_one()


def get_all_books(
    session: Session, skip: int = 0, limit: int = 10, author_id: int | None = None
) -> Sequence[models.Book]:
    stmt = select(models.Book).order_by(models.Book.id)
    if author_id is not None:
        stmt = stmt.where(models.Book.author_id == author_id)
    stmt = stmt.offset(skip).limit(limit)
    return session.execute(stmt).scalars().all()


def create_book(session: Session, data: BookCreateSchema) -> models.Book:
    book = models.Book(**data.model_dump())
    session.add(book)
    session.commit()
    session.refresh(book)
    return book


def count_books(session: Session, author_id: int | None = None) -> int:
    stmt = select(func.count()).select_from(models.Book)
    if author_id is not None:
        stmt = stmt.where(models.Book.author_id == author_id)
    return session.execute(stmt).scalar_one()
