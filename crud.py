from sqlalchemy.orm import Session

import models
import schemas


def create_author(db: Session, author: schemas.AuthorCreate) -> models.Author:
    db_author = models.Author(**author.model_dump())
    db.add(db_author)
    db.commit()
    db.refresh(db_author)
    return db_author


def get_authors(
    db: Session,
    skip: int = 0,
    limit: int = 100,
) -> list[models.Author]:
    return db.query(models.Author).offset(skip).limit(limit).all()


def get_author(db: Session, author_id: int) -> models.Author | None:
    return db.query(models.Author).filter(models.Author.id == author_id).first()


def create_book(
    db: Session,
    book: schemas.BookCreate,
    author_id: int,
) -> models.Book:
    book_data = book.model_dump(exclude_none=True)
    db_book = models.Book(**book_data, author_id=author_id)
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book


def get_books(
    db: Session,
    skip: int = 0,
    limit: int = 100,
    author_id: int | None = None,
) -> list[models.Book]:
    query = db.query(models.Book)
    if author_id is not None:
        query = query.filter(models.Book.author_id == author_id)
    return query.offset(skip).limit(limit).all()
