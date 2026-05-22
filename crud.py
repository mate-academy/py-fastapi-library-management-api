from fastapi import HTTPException
from sqlalchemy.orm import Session

import models
import schemas


def get_all_books(db: Session,  skip: int, limit: int, author_id: int | None = None):
    queryset = db.query(models.Book)

    if author_id:
        queryset = queryset.filter(
            models.Book.author_id == author_id
        )

    return queryset.offset(skip).limit(limit).all()


def get_book_by_id(db: Session, id: int):
    return db.query(models.Book).get(id)


def get_book_by_title(db: Session, title: str):
    return db.query(models.Book).filter(
        models.Book.title == title,
    ).first()


def create_book(db: Session, book: schemas.BookCreate):
    db_book = models.Book(
        title=book.title,
        summary=book.summary,
        publication_date=book.publication_date,
        author_id=book.author,
    )

    db.add(db_book)
    db.commit()
    db.refresh(db_book)

    return db_book


def get_all_authors(db: Session, skip: int, limit: int, ):
    return db.query(models.Author).offset(skip).limit(limit).all()


def get_author_by_id(db: Session, id: int):
    return db.query(models.Author).get(id)


def get_author_by_name(db: Session, name: str):
    return db.query(models.Author).filter(
        models.Author.name == name,
    ).first()


def create_author(db: Session, author: schemas.AuthorCreate):
    db_author = models.Author(
        name=author.name,
        bio=author.bio,
    )

    db.add(db_author)
    db.commit()
    db.refresh(db_author)

    return db_author
