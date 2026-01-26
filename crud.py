from sqlalchemy.orm import Session
from sqlalchemy import select
from db import models
import schemas


def get_author_by_name(db: Session, name: str):
    return db.scalar(select(models.Author).where(models.Author.name == name))

def get_author(db: Session, author_id: int):
    return db.get(models.Author, author_id)


def get_authors(db: Session, skip: int = 0, limit: int = 10):
    query = select(models.Author).offset(skip).limit(limit)
    return db.scalars(query).all()


def create_author(db: Session, author: schemas.AuthorCreate):
    db_author = models.Author(**author.model_dump())
    db.add(db_author)
    db.commit()
    db.refresh(db_author)
    return db_author


def get_books(db: Session, skip: int = 0, limit: int = 10, author_id: int = None):
    query = select(models.Book)

    if author_id:
        query = query.where(models.Book.author_id == author_id)

    query = query.offset(skip).limit(limit)

    return db.scalars(query).all()


def create_book(db: Session, book: schemas.BookCreate):
    db_book = models.Book(**book.model_dump())
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book
