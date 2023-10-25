from sqlalchemy.orm import Session
from schemas import AuthorCreate, Book, BookCreate

import models


def get_all_authors(db: Session) -> list[models.Author]:
    return db.query(models.Author).all()


def get_author_by_id(db: Session, author_id: int) -> models.Author:
    return db.query(models.Author).filter(
        models.Author.id == author_id
    ).first()


def create_author(db: Session, author: AuthorCreate) -> models.Author:
    db_author = models.Author(
        name=author.name,
        bio=author.bio
    )
    db.add(db_author)
    db.commit()
    db.refresh(db_author)

    return db_author


def get_all_books(db: Session, author_id: int) -> list[models.Book]:
    queryset = db.query(models.Book)

    if author_id:
        queryset = queryset.filter(models.Book.author_id == author_id)

    return queryset.all()


def get_book_by_id(db: Session, book_id: int) -> models.Book:
    return db.query(models.Book).filter(
        models.Book.id == book_id
    ).first()


def create_book(db: Session, book: BookCreate, author_id: int) -> models.Book:
    db_book = models.Book(
        title=book.title,
        summary=book.summary,
        publication_date=book.publication_date,
        author_id=author_id
    )
    db.add(db_book)
    db.commit()
    db.refresh(db_book)

    return db_book
