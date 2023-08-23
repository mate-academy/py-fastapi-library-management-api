from sqlalchemy.orm import Session

import schemas
from db import models


def get_all_authors(db: Session, skip: int, limit: int):
    return db.query(models.DBAuthor).offset(skip).limit(limit).all()


def get_author(db: Session, author_id: int):
    return (
        db.query(models.DBAuthor)
        .filter(models.DBAuthor.id == author_id).first()
    )


def get_author_by_name(db: Session, name: str):
    return (
        db.query(models.DBAuthor)
        .filter(models.DBAuthor.name == name).first()
    )


def create_author(db: Session, author: schemas.AuthorCreate):
    db_author = models.DBAuthor(
        name=author.name,
        bio=author.bio
    )
    db.add(db_author)
    db.commit()
    db.refresh(db_author)

    return db_author


def get_all_books(
        db: Session, skip: int, limit: int, author_id: int | None = None
):
    queryset = db.query(models.DBBook)

    if author_id:
        queryset = queryset.filter(models.DBBook.author_id == author_id)

    return queryset.offset(skip).limit(limit).all()


def create_book(db: Session, book: schemas.BookCreate):
    db_book = models.DBBook(
        title=book.title,
        summary=book.summary,
        publication_date=book.publication_date,
        author_id=book.author_id
    )
    db.add(db_book)
    db.commit()
    db.refresh(db_book)

    return db_book
