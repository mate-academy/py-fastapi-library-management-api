from http.client import HTTPException

from sqlalchemy.orm import Session

import schemas
from db import models
from schemas import AuthorCreate


def get_authors_with_pagination(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.Author).offset(skip).limit(limit).all()


def get_author_by_name(db: Session, name: str):
    return db.query(models.Author).filter(models.Author.name == name).first()


def get_author_by_id(db: Session, author_id: int):
    return db.query(models.Author).filter(models.Author.id == author_id).first()


def update_author(db: Session, author_id: int, updated_author: schemas.AuthorUpdate):

    author = db.query(models.Author).filter(models.Author.id == author_id).first()

    if not author:
        return None

    for key, value in updated_author.dict(exclude_unset=True).items():
        setattr(author, key, value)

    db.commit()
    db.refresh(author)
    return author


def delete_author(db: Session, author_id: int):

    author = db.query(models.Author).filter(models.Author.id == author_id).first()

    if not author:
        return None

    db.delete(author)
    db.commit()


def create_author(db: Session, author: schemas.AuthorCreate):
    new_author = models.Author(
        name=author.name,
        bio=author.bio
    )
    db.add(new_author)
    db.commit()
    db.refresh(new_author)
    return new_author


def get_books_with_pagination(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.Book).offset(skip).limit(limit).all()


def get_books_by_author(db: Session, author_id: int, skip: int = 0, limit: int = 10):

    return (
        db.query(models.Book)
        .filter(models.Book.author_id == author_id)
        .offset(skip)
        .limit(limit)
        .all()
    )


def get_book_by_title(db: Session, title: str):
    return db.query(models.Book).filter(models.Book.title == title).first()


def get_book_by_id(db: Session, book_id: int):
    return db.query(models.Book).filter(models.Book.id == book_id).first()


def update_book(db: Session, book_id: int, updated_book: schemas.BookUpdate):
    book = db.query(models.Book).filter(models.Book.id == book_id).first()

    if not book:
        return None

    for key, value in updated_book.dict(exclude_unset=True).items():
        setattr(book, key, value)

    db.commit()
    db.refresh(book)
    return book


def delete_book(db: Session, book_id: int):
    book = db.query(models.Book).filter(models.Book.id == book_id).first()

    if not book:
        return None

    db.delete(book)
    db.commit()


def create_book(db: Session, book: schemas.BookCreate):
    new_book = models.Book(
        title=book.title,
        summary=book.summary,
        publication_date=book.publication_date,
        author_id=book.author_id
    )
    db.add(new_book)
    db.commit()
    db.refresh(new_book)
    return new_book
