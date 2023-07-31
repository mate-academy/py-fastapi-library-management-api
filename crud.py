from typing import Optional, List

from sqlalchemy.orm import Session

import models
import schemas


def get_author(db: Session, author_id: int) -> Optional[models.DBAuthor]:
    return db.query(models.DBAuthor).filter(models.DBAuthor.id == author_id).first()


def get_author_by_name(db: Session, name: str) -> Optional[models.DBAuthor]:
    return db.query(models.DBAuthor).filter(models.DBAuthor.name == name).first()


def get_authors(
    db: Session, skip: int = 0, limit: int = 100
) -> Optional[List[models.DBAuthor]]:
    return db.query(models.DBAuthor).offset(skip).limit(limit).all()


def create_author(db: Session, author: schemas.AuthorCreate) -> models.DBAuthor:
    db_author = models.DBAuthor(
        name=author.name,
        bio=author.bio,
    )
    db.add(db_author)
    db.commit()
    db.refresh(db_author)

    return db_author


def delete_author(db: Session, author_id: int) -> Optional[models.DBAuthor]:
    db_author = get_author(db, author_id)

    if db_author is not None:
        db.delete(db_author)
        db.commit()

        return db_author


def update_author(
    db: Session, author_id: int, updated_data: dict
) -> Optional[models.DBAuthor]:
    db_author = get_author(db, author_id)

    if db_author:
        for key, value in updated_data.items():
            setattr(db_author, key, value)

        db.commit()
        db.refresh(db_author)

    return db_author


def get_book(db: Session, book_id: int) -> Optional[models.DBBook]:
    return db.query(models.DBBook).filter(models.DBBook.id == book_id).first()


def get_book_by_title(db: Session, title: str) -> Optional[models.DBBook]:
    return db.query(models.DBBook).filter(models.DBBook.title == title).first()


def get_books(
    db: Session, skip: int = 0, limit: int = 100, author_id: Optional[int] = None
) -> Optional[List[models.DBBook]]:
    queryset = db.query(models.DBBook).join(models.DBAuthor)

    if author_id is not None:
        queryset = queryset.filter(models.DBBook.author_id == author_id)

    return queryset.offset(skip).limit(limit).all()


def create_author_book(
    db: Session, book: schemas.BookCreate, author_id: int
) -> models.DBBook:
    db_book = models.DBBook(
        **book.model_dump(),
        author_id=author_id,
    )
    db.add(db_book)
    db.commit()
    db.refresh(db_book)

    return db_book


def delete_book(db: Session, book_id: int) -> models.DBBook:
    db_book = get_book(db, book_id)

    if db_book:
        db.delete(db_book)
        db.commit()

    return db_book


def update_book(db: Session, book_id: int, updated_data: dict) -> models.DBBook:
    db_book = get_book(db, book_id)

    if db_book:
        for key, value in updated_data.items():
            setattr(db_book, key, value)

        db.commit()
        db.refresh(db_book)

    return db_book


def create_book(db: Session, book: schemas.BookCreate) -> models.DBBook:
    db_book = models.DBBook(**book.model_dump())
    db.add(db_book)
    db.commit()
    db.refresh(db_book)

    return db_book
