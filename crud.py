from sqlalchemy.orm import Session
from db import models

import schemas


def get_author(db: Session, author_id: int) -> models.Author:
    return db.query(models.Author).filter(models.Author.id == author_id).first()


def get_all_authors(db: Session) -> list[models.Author]:
    return db.query(models.Author).all()


def create_author(db: Session, author: schemas.AuthorCreate) -> models.Author:
    db_author = models.Author(name=author.name, bio=author.bio)
    db.add(db_author)
    db.commit()
    db.refresh(db_author)
    return db_author


def get_books_by_author(db: Session, author_id: int) -> list[models.Book]:
    query = db.query(models.Book)
    if author_id:
        query = query.filter(models.Book.author_id == author_id)
    return query.all()


def get_all_books(db: Session) -> list[models.Book]:
    return db.query(models.Book).all()


def create_book(db: Session, book: schemas.BookCreate) -> listmodels.Book:
    db_book = models.Book(
        title=book.title,
        summary=book.summary,
        author_id=book.author_id
    )
    db_book.set_publication_date(book.publication_date)
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book
