from sqlalchemy.orm import Session
from db import models

import schemas


# Author

def author_create(
        db: Session,
        author: schemas.AuthorCreate
        ):
    
    db_author = models.DBAuthor(
        name=author.name,
        bio=author.bio
    )
    db.add(db_author)
    db.commit()
    db.refresh(db_author)
    return db_author


def get_author_list(
        db: Session,
        skip: int | None = None,
        limit: int | None = None
        ):
    queryset = db.query(models.DBAuthor)

    if skip is not None:
        queryset = queryset.offset(skip)

    if limit is not None:
        queryset = queryset.limit(limit)
    
    return queryset.all()


def get_author_by_id(
        db: Session,
        id: int
):
    return db.query(models.DBAuthor).filter(models.DBAuthor.id==id).first()


def get_author_by_name(
        db: Session,
        name: str
):
    return db.query(models.DBAuthor).filter(models.DBAuthor.name==name).first()


# Book

def book_create(
        db: Session,
        book: schemas.BookCreate
):
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


def get_book_list(
        db: Session,
        skip: int | None = None,
        limit: int | None = None
):
    queryset = db.query(models.DBBook)

    if skip is not None:
        queryset = queryset.offset(skip)

    if limit is not None:
        queryset = queryset.limit(limit)
    
    return queryset.all()


def get_book_by_author_id(
        db: Session,
        author_id: int
):
    return db.query(models.DBBook).filter(models.DBBook.author_id==author_id).all()
