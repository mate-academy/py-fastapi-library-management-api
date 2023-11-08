from sqlalchemy.orm import Session

import schemas
from db import models


def get_all_authors(db: Session, skip: int = 0, limit: int = 5):
    return db.query(models.Author).offset(skip).limit(limit).all()


def get_author_by_id(db: Session, author_id: int):
    return db.query(models.Author).filter(
        models.Author.id == author_id
    ).first()


def create_author(db: Session, author_schemas: schemas.AuthorCreate):
    author = models.Author(
        name=author_schemas.name,
        bio=author_schemas.bio,
    )
    db.add(author)
    db.commit()
    db.refresh(author)

    return author


def get_all_books(db: Session, skip: int = 0, limit: int = 5):
    return db.query(models.Book).offset(skip).limit(limit).all()


def get_book_by_id(db: Session, book_id: int):
    return db.query(models.Book).filter(
        models.Book.id == book_id
    ).first()


def get_book_by_author_id(db: Session, author_id: int):
    return db.query(models.Book).filter(
        models.Book.author_id == author_id
    ).all()


def create_book(
        db: Session,
        book_schemas: schemas.BookCreate,
):
    book = models.Book(
        title=book_schemas.title,
        summary=book_schemas.summary,
        publication_date=book_schemas.publication_date,
        author_id=book_schemas.author_id,
    )
    db.add(book)
    db.commit()
    db.refresh(book)

    return book
