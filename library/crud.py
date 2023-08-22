from typing import List

from sqlalchemy.orm import Session
from library import models, schemas


def post_author(
        db: Session,
        author: schemas.AuthorCreate
) -> schemas.Author:
    new_author = models.Author(
        **author.model_dump()
    )

    db.add(new_author)
    db.commit()
    db.refresh(new_author)

    return new_author


def get_authors(
        db: Session,
        skip: int = 0,
        limit: int = 100
) -> List[schemas.Author]:
    return db.query(
        models.Author
    ).offset(skip).limit(limit).all()


def get_author_by_id(
        db: Session,
        author_id: int
) -> schemas.Author:
    return db.query(
        models.Author
    ).filter(models.Author.id == author_id).first()


def post_book(
        db: Session,
        book: schemas.BookCreate,
) -> schemas.Book:
    new_book = models.Book(
        **book.model_dump(),
    )

    db.add(new_book)
    db.commit()
    db.refresh(new_book)

    return new_book


def get_books(
        db: Session,
        skip: int = 0,
        limit: int = 100
) -> List[schemas.Book]:
    return db.query(
        models.Book
    ).offset(skip).limit(limit).all()


def get_books_by_author_id(
        db: Session,
        author_id: int,
        skip: int = 0,
        limit: int = 0
) -> List[schemas.Book]:
    return db.query(
        models.Book
    ).filter(
        models.Book.author_id == author_id
    ).offset(skip).limit(limit).all()
