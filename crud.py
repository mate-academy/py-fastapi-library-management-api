from sqlalchemy.orm import Session

from db import models
from schemas import AuthorCreate, BookCreate


def create_author(db: Session, author: AuthorCreate) -> models.Author:
    db_author = models.Author(**author.model_dump())
    db.add(db_author)
    db.commit()

    db.refresh(db_author)

    return db_author


def get_author(db: Session, author_id: int) -> models.Author:
    return (
        db.query(models.Author).filter(models.Author.id == author_id).first()
    )


def get_author_list(
    db: Session, skip: int = 0, limit: int = 10
) -> list[models.Author]:
    return db.query(models.Author).offset(skip).limit(limit).all()


def update_author(
    db: Session, author_id: int, author: AuthorCreate
) -> models.Author:
    db_author = (
        db.query(models.Author).filter(models.Author.id == author_id).first()
    )
    if db_author:
        for key, value in author.dict().items():
            setattr(db_author, key, value)
        db.commit()
        db.refresh(db_author)

    return db_author


def delete_author(db: Session, author_id: int) -> bool:
    db_author = (
        db.query(models.Author).filter(models.Author.id == author_id).first()
    )
    if db_author:
        db.delete(db_author)
        db.commit()
        return True

    return False


def create_book(db: Session, book: BookCreate) -> models.Book:
    db_book = models.Book(**book.model_dump())
    db.add(db_book)
    db.commit()
    db.refresh(db_book)

    return db_book


def get_book(db: Session, book_id: int) -> models.Book:
    return db.query(models.Book).filter(models.Book.id == book_id).first()


def get_book_list(
    db: Session,
    author_id: int | None = None,
    skip: int = 0,
    limit: int = 10
) -> list[models.Book]:
    query = db.query(models.Book)

    if author_id:
        query = query.filter(models.Book.author_id == author_id)

    return query.offset(skip).limit(limit).all()


def update_book(db: Session, book_id: int, book: BookCreate) -> models.Book:
    db_book = db.query(models.Book).filter(models.Book.id == book_id).first()
    if db_book:
        for key, value in book.dict().items():
            setattr(db_book, key, value)
        db.commit()
        db.refresh(db_book)
    return db_book


def delete_book(db: Session, book_id: int) -> bool:
    db_book = db.query(models.Book).filter(models.Book.id == book_id).first()
    if db_book:
        db.delete(db_book)
        db.commit()
        return True
    return False
