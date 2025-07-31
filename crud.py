from typing import List, Optional

from sqlalchemy.orm import Session

import models
import schemas


def get_author_by_id(db: Session, author_id: int) -> Optional[models.Author]:
    return db.query(models.Author).filter(models.Author.id == author_id).first()

def get_author_by_name(db: Session, name: str) -> Optional[models.Author]:
    return db.query(models.Author).filter(models.Author.name == name).first()

def get_all_authors(db: Session, skip: int = 0, limit: int = 10) -> List[models.Author]:
    return db.query(models.Author).offset(skip).limit(limit).all()

def create_author(db: Session, author: schemas.AuthorCreate) -> models.Author:
    db_author = models.Author(name=author.name, bio=author.bio)
    db.add(db_author)
    db.commit()
    db.refresh(db_author)

    return db_author

def update_author(db: Session, author_id: int, author: schemas.AuthorCreate) -> Optional[models.Author]:
    db_author = get_author_by_id(db, author_id)

    if db_author:
        db_author.name = author.name
        db_author.bio = author.bio
        db.commit()
        db.refresh(db_author)

        return db_author

    return None

def get_book_by_id(db: Session, book_id: int) -> Optional[models.Book]:
    return db.query(models.Book).filter(models.Book.id == book_id).first()

def get_book_by_name(db: Session, name: str) -> Optional[models.Book]:
    return db.query(models.Book).filter(models.Book.title == name).first()

def get_all_books(db: Session, skip: int = 0, limit: int = 10) -> List[models.Book]:
    return db.query(models.Book).offset(skip).limit(limit).all()

def get_books_by_author_id(db: Session, author_id: int, skip: int = 0, limit: int = 10) -> List[models.Book]:
    return db.query(models.Book).filter(models.Book.author_id == author_id).offset(skip).limit(limit).all()

def create_book(db: Session, book: schemas.BookCreate) -> models.Book:
    db_book = models.Book(
        title=book.title,
        summary=book.summary,
        publication_date=book.publication_date,
        author_id=book.author_id
    )
    db.add(db_book)
    db.commit()
    db.refresh(db_book)

    return db_book

def update_book(db: Session, book_id: int, book: schemas.BookCreate) -> Optional[models.Book]:
    db_book = get_book_by_id(db, book_id)

    if db_book:
        db_book.title = book.title
        db_book.summary = book.summary
        db_book.publication_date = book.publication_date
        db_book.author_id = book.author_id
        db.commit()
        db.refresh(db_book)

        return db_book

    return None