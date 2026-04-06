from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session
from typing import Sequence
import schemas
from db import models


def get_all_books(
    db: Session,
    author_id: int | None = None,
    skip: int = 0,
    limit: int = 10,
) -> Sequence[models.Book]:

    query = select(models.Book)

    if author_id is not None:
        query = query.where(models.Book.author_id == author_id)

    query = query.offset(skip).limit(limit)

    return db.scalars(query).all()


def get_author_by_id(
    db: Session,
    author_id: int
) -> models.Author | None:
    author = db.execute(
        select(models.Author).where(models.Author.id == author_id)
    ).scalar_one_or_none()
    if not author:
        raise HTTPException(status_code=404, detail="Author not found")
    return author


def create_book(
    db: Session,
    book: schemas.BookCreateSchema
) -> models.Book:
    author = db.execute(
        select(models.Author).where(models.Author.id == book.author_id)
    ).scalar_one_or_none()

    if not author:
        raise HTTPException(status_code=404, detail="Author not found")
    db_book = models.Book(
        title=book.title,
        summary=book.summary,
        publication_date=book.publication_date,
        author_id=book.author_id
    )
    db.add(db_book)
    db.commit()
    db.refresh(db_book)

    return db_book


def create_author(
    db: Session,
    author: schemas.AuthorSchemaBase
) -> models.Author:

    db_author = models.Author(
        name=author.name,
        bio=author.bio,
    )
    db.add(db_author)
    db.commit()
    db.refresh(db_author)

    return db_author


def get_authors_list(db, skip: int, limit: int) -> list[models.Author]:
    return db.scalars(
        select(models.Author)
        .offset(skip)
        .limit(limit)
    ).all()
