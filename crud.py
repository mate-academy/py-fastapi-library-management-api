from sqlalchemy import select
from sqlalchemy.orm import Session

import models
import schemas


def get_author(db: Session, author_id: int):
    return db.get(models.Author, author_id)


def get_author_by_name(db: Session, name: str):
    return db.scalar(select(models.Author).where(models.Author.name == name))


def create_author(db: Session, author: schemas.AuthorCreate):
    obj = models.Author(**author.model_dump())
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj


def get_authors(db: Session, skip: int, limit: int):
    query = (
        select(models.Author).order_by(models.Author.id)
        .offset(skip).limit(limit)
    )
    return db.scalars(query).all()


def create_book(db: Session, book: schemas.BookCreate, author_id: int):
    obj = models.Book(**book.model_dump(), author_id=author_id)
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj


def get_books(db: Session, skip: int, limit: int, author_id: int | None):
    query = select(models.Book)
    if author_id is not None:
        query = query.where(models.Book.author_id == author_id)
    query = query.order_by(models.Book.id).offset(skip).limit(limit)
    return db.scalars(query).all()
