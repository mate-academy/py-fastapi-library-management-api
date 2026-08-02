from sqlalchemy import select
from sqlalchemy.orm import Session

import models
import schemas

def get_author(db: Session, author_id: int) -> models.Author | None:
    return db.scalar(select(models.Author).where(models.Author.id == author_id))

def get_author_by_name(db: Session, name: str) -> models.Author | None:
    return db.scalar(select(models.Author).where(models.Author.name == name))

def get_authors(db: Session, skip: int = 0, limit: int = 10) -> list[models.Author]:
    return list(db.scalars(select(models.Author).offset(skip).limit(limit)).unique().all())

def create_author(db: Session, author: schemas.AuthorCreate) -> models.Author:
    db_author = models.Author(name=author.name, bio=author.bio)
    db.add(db_author)
    db.commit()
    db.refresh(db_author)
    return db_author

def get_books(db: Session, skip: int = 0, limit: int = 10) -> list[models.Book]:
    return list(db.scalars(select(models.Book).offset(skip).limit(limit)).all())

def get_books_by_author(db: Session, author_id: int) -> list[models.Book]:
    return list(db.scalars(select(models.Book).where(models.Book.author_id == author_id)).all())

def create_book(db: Session, book: schemas.BookCreate, author_id: int) -> models.Book:
    db_book = models.Book(
        title=book.title,
        summary=book.summary,
        publication_date=book.publication_date,
        author_id=author_id
    )
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book
