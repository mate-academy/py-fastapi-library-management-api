from typing import List

from sqlalchemy.orm import Session

import schemas
import models


def get_all_authors(
        db: Session,
        skip: int = 0,
        limit: int = 10,
) -> List[type[models.Author]]:
    return db.query(models.Author).offset(skip).limit(limit).all()

def get_author_by_id(author_id: int, db: Session) -> type[models.Author]:
    return (db.query(models.Author).
            filter(models.Author.id == author_id).first())

def get_author_by_name(author_name: str, db: Session) -> type[models.Author]:
    return (db.query(models.Author).
            filter(models.Author.name == author_name).first())

def create_author(
        author: schemas.AuthorCreate,
        db: Session
) -> models.Author:
    db_author = models.Author(
        name=author.name,
        bio=author.bio,
    )
    db.add(db_author)
    db.commit()
    db.refresh(db_author)

    return db_author

def get_all_books(
        db: Session,
        skip: int = 0,
        limit: int = 10,
        author_id: int | None = None
) -> List[type[models.Book]]:
    query = db.query(models.Book)
    if author_id:
        query = query.filter(models.Book.author_id == author_id)

    return query.offset(skip).limit(limit).all()

def get_book(book_id: int, db: Session) -> type[models.Book]:
    return db.query(models.Book).filter(models.Book.id == book_id).first()

def create_book(
        book: schemas.BookCreate,
        db: Session
) -> models.Book:
    db_book = models.Book(
        title=book.title,
        summary=book.summary,
        publication_date=book.publication_date,
        author_id=book.author_id,
    )
    db.add(db_book)
    db.commit()
    db.refresh(db_book)

    return db_book
