from sqlalchemy.orm import Session
from typing import List, Optional

import schemas
from db import models


def get_author(db: Session, author_id: int) -> Optional[models.Author]:
    return db.query(models.Author).filter(models.Author.id == author_id).first()


def get_author_by_name(db: Session, name: str) -> Optional[models.Author]:
    return db.query(models.Author).filter(models.Author.name == name).first()


def get_authors(db: Session, skip: int = 0, limit: int = 100) -> List[models.Author]:
    return db.query(models.Author).offset(skip).limit(limit).all()


def create_author(db: Session, author: schemas.AuthorCreate) -> models.Author:
    db_author = models.Author(name=author.name, bio=author.bio)
    db.add(db_author)
    db.commit()
    db.refresh(db_author)
    return db_author


def get_book(db: Session, book_id: int) -> Optional[models.Book]:
    return db.query(models.Book).filter(models.Book.id == book_id).first()


def get_books(db: Session, skip: int = 0, limit: int = 100) -> List[models.Book]:
    return db.query(models.Book).offset(skip).limit(limit).all()


def create_author_book(
    db: Session, book: schemas.BookCreate, author_id: int
) -> models.Book:
    db_book = models.Book(**book.model_dump(), author_id=author_id)
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book


def delete_book(db: Session, book_id: int) -> Optional[models.Book]:
    book_to_delete = db.query(models.Book).filter(models.Book.id == book_id).first()
    if book_to_delete:
        db.delete(book_to_delete)
        db.commit()
        return book_to_delete
    return None


def update_book(
    db: Session, book_id: int, book: schemas.BookCreate
) -> Optional[models.Book]:
    book_to_update = db.query(models.Book).filter(models.Book.id == book_id).first()
    if book_to_update:
        book_to_update.title = book.title
        book_to_update.summary = book.summary
        book_to_update.publication_date = book.publication_date
        db.commit()
        db.refresh(book_to_update)
        return book_to_update
    return None


def delete_author(db: Session, author_id: int) -> Optional[models.Author]:
    author_to_delete = (
        db.query(models.Author).filter(models.Author.id == author_id).first()
    )
    if author_to_delete:
        # Cascade delete is handled by the relationship configuration in models.py
        db.delete(author_to_delete)
        db.commit()
        return author_to_delete
    return None


def update_author(
    db: Session, author_id: int, author: schemas.AuthorCreate
) -> Optional[models.Author]:
    author_to_update = (
        db.query(models.Author).filter(models.Author.id == author_id).first()
    )
    if author_to_update:
        # Update the author fields
        author_to_update.name = author.name
        author_to_update.bio = author.bio
        db.commit()
        db.refresh(author_to_update)
        return author_to_update
    return None

def get_books_by_author(db: Session, author_id: int, skip: int = 0, limit: int = 100):
    return db.query(models.Book).filter(models.Book.author_id == author_id).offset(skip).limit(limit).all()
