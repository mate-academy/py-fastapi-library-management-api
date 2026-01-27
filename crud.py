from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

import models
import schemas


def get_record_by_name(
    db: Session, model: type[models.Base], name: str, raise_if_exists: bool = False
) -> models.Base | None:
    field = getattr(model, "name", None) or getattr(model, "title", None)
    record = db.scalars(select(model).where(field == name)).first()

    if raise_if_exists and record:
        raise HTTPException(
            status_code=400,
            detail=f"{model.__name__} with name '{name}' already exists",
        )

    return record


def get_authors(db: Session, skip: int = 0, limit: int = 100) -> list[models.Author]:
    query = select(models.Author).offset(skip).limit(limit)

    return list(db.scalars(query).all())


def get_author_by_id(db: Session, author_id: int) -> models.Author:
    author: models.Author | None = db.get(models.Author, author_id)
    if author is None:
        raise HTTPException(
            status_code=404, detail=f"Author with id {author_id} does not exist"
        )

    return author


def create_author(db: Session, author_data: schemas.AuthorCreate) -> models.Author:
    get_record_by_name(db, models.Author, name=author_data.name, raise_if_exists=True)
    new_author = models.Author(**author_data.model_dump())
    db.add(new_author)
    db.commit()
    db.refresh(new_author)

    return new_author


def get_books(
    db: Session, author_id: int, skip: int = 0, limit: int = 100
) -> list[models.Book]:
    query = select(models.Book)
    if author_id is not None:
        query = query.where(models.Book.author_id == author_id)

    return list(db.scalars(query.offset(skip).limit(limit)).all())


def create_book(db: Session, book_data: schemas.BookCreate) -> models.Book:
    get_record_by_name(db, models.Book, name=book_data.title, raise_if_exists=True)
    get_author_by_id(db, author_id=book_data.author_id)
    new_book = models.Book(**book_data.model_dump())
    db.add(new_book)
    db.commit()
    db.refresh(new_book)

    return new_book
