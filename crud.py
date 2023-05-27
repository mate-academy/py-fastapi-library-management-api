from typing import Optional

from fastapi import HTTPException
from sqlalchemy.orm import Session

import models
import schemas


def get_all_authors(
        db: Session,
        skip: int = 0,
        limit: int = 0,
) -> list[models.Author]:
    return db.query(models.Author).offset(skip).limit(limit).all()


def create_author(db: Session, author: schemas.AuthorCreate) -> models.Author:
    db_author = db.query(models.Author).filter(models.Author.name == author.name).first()

    if db_author:
        raise HTTPException(status_code=400, detail="Author is already exist")

    author = models.Author(
        name=author.name,
        bio=author.bio,
    )

    db.add(author)
    db.commit()
    db.refresh(author)

    return author


def get_author_by_id(db: Session, author_id: models.Author.id) -> Optional[models.Author]:
    db_author = db.query(models.Author).filter(models.Author.id == author_id).first()

    if db_author is None:
        raise HTTPException(status_code=404, detail="Author not found")

    return db_author


def update_author(db: Session, author_id: int, author: schemas.AuthorUpdate) -> models.Author:
    db_author = db.query(models.Author).filter(models.Author.id == author_id).first()

    if db_author is None:
        raise HTTPException(status_code=404, detail="Author not found")

    for field, value in author.dict(exclude_unset=True).items():
        setattr(db_author, field, value)

    db.commit()
    db.refresh(db_author)

    return db_author


def delete_author(db: Session, author_id: int) -> None:
    author = db.query(models.Author).filter(models.Author.id == author_id).first()

    if author is None:
        raise HTTPException(status_code=404, detail="Author not found")

    db.delete(author)
    db.commit()


def get_all_books(
        db: Session,
        skip: int = 0,
        limit: int = 0,
) -> list[models.Book]:

    return db.query(models.Book).offset(skip).limit(limit).all()


def create_book(db: Session, book: schemas.BookCreate) -> models.Book:
    db_book = db.query(models.Book).filter(models.Book.title == book.title).first()

    if db_book:
        raise HTTPException(status_code=400, detail="Book is already exist")

    book = models.Book(
        title=book.title,
        summary=book.summary,
        publication_date=book.publication_date,
        author_id=book.author_id,
    )

    db.add(book)
    db.commit()
    db.refresh(book)

    return book


def get_book_by_id(db: Session, book_id: models.Book.id) -> Optional[models.Book]:
    db_book = db.query(models.Book).filter(models.Book.id == book_id).first()

    if db_book is None:
        raise HTTPException(status_code=404, detail="Book not found")

    return db.query(models.Book).filter(models.Book.id == book_id).first()


def update_book(db: Session, book_id: int, book: schemas.BookUpdate) -> models.Book:
    db_book = db.query(models.Book).filter(models.Book.id == book_id).first()

    if db_book is None:
        raise HTTPException(status_code=404, detail="Author not found")

    for field, value in book.dict(exclude_unset=True).items():
        setattr(db_book, field, value)

    db.commit()
    db.refresh(db_book)

    return db_book


def delete_book(db: Session, book_id: int) -> None:
    book = db.query(models.Book).filter(models.Book.id == book_id).first()

    if book is None:
        raise HTTPException(status_code=404, detail="Book not found")

    db.delete(book)
    db.commit()
