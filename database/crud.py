from typing import Optional

from sqlalchemy.orm import Session

import database.models
import schemas


def get_all_books(db: Session, skip: int, limit: int) -> list[database.models.Book]:
    return db.query(database.models.Book).offset(skip).limit(limit).all()


def get_all_authors(db: Session, skip: int, limit: int) -> list[database.models.Author]:
    return db.query(database.models.Author).offset(skip).limit(limit).all()


def create_book(db: Session, book: schemas.BookCreateSchema) -> database.models.Book:
    db_book = database.models.Book(title=book.title,
                                   summary=book.summary,
                                   publication_date=book.publication_date,
                                   author_id=book.author_id,
                                   )
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book


def create_author(db: Session, author: schemas.AuthorCreateSchema) -> database.models.Author:
    db_author = database.models.Author(name=author.name, bio=author.bio)
    db.add(db_author)
    db.commit()
    db.refresh(db_author)
    return db_author


def get_author_by_id(db: Session, author_id: int) -> Optional[database.models.Author]:
    return db.query(database.models.Author).filter(database.models.Author.id == author_id).first()


def get_books_by_author_id(db: Session, author_id: int) -> list[database.models.Book]:
    return db.query(database.models.Book).filter(database.models.Book.author_id == author_id).all()


def get_author_by_name(db: Session, name: str):
    return db.query(database.models.Author).filter(database.models.Author.name == name).first()
