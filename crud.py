from sqlalchemy.orm import Session

import models
import schemas


def get_author_by_name(db: Session, name: str) -> models.Author:
    return (
        db.query(models.Author).filter(models.Author.name == name).first()
    )


def get_authors(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.Author).offset(skip).limit(limit).all()


def get_author(db: Session, author_id: int):
    return db.query(models.Author).filter(models.Author.id == author_id).first()


def create_author(db: Session, author: schemas.AuthorCreate):
    db_author = models.Author(**author.dict())

    db.add(db_author)
    db.commit()
    db.refresh(db_author)

    return db_author


def create_book(db: Session, book: schemas.BookCreate):
    db_book = models.Book(**book.dict())
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book


def get_books(
        db: Session,
        skip: int = 0,
        limit: int = 10,
        author_id: int | None = None
):
    books = db.query(models.Book).offset(skip).limit(limit).all()

    if author_id:
        books = books.filter(models.Book.author_id == author_id)

    return books
