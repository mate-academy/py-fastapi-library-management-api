from sqlalchemy import select
from sqlalchemy.orm import Session

import models
import schemas


def get_authors(db: Session, skip: int = 0, limit: int = 10):
    return db.scalars(
        select(models.Author).offset(skip).limit(limit)
    ).all()

def get_author_by_id(db: Session, author_id: int):
    return db.scalars(select(models.Author).where(models.Author.id == author_id)).first()

def create_author(db: Session, author: schemas.AuthorCreate):
    db_author = models.Author(
        name=author.name,
        bio=author.bio
    )
    db.add(db_author)
    db.commit()
    db.refresh(db_author)

    return db_author

def get_books(db: Session, skip: int = 0, limit: int = 10):
    return db.scalars(select(models.Book).offset(skip).limit(limit)).all()

def get_book_by_author_id(db: Session, author_id: int):
    return db.scalars(select(models.Book).where(models.Book.author_id == author_id)).first()

def create_book(db: Session, book: schemas.BookCreate, author_id: int):
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
