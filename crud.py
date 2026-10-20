from sqlalchemy.orm import Session

import models
import schemas


def get_authors(db: Session, skip: int, limit: int):
    return db.query(models.DBAuthor).offset(skip).limit(limit).all()


def create_author(db: Session, author: schemas.AuthorCreate):
    db_author = models.DBAuthor(**author.model_dump())

    db.add(db_author)
    db.commit()
    db.refresh(db_author)

    return db_author


def get_author_detail(db: Session, author_id: int):
    return db.query(models.DBAuthor).filter(models.DBAuthor.id == author_id).first()


def create_book(db: Session, book: schemas.BookCreate):
    db_book = models.DBBook(**book.model_dump())

    db.add(db_book)
    db.commit()
    db.refresh(db_book)

    return db_book


def get_books(db: Session, skip: int, limit: int, author_id: int | None):
    queryset = db.query(models.DBBook)

    if author_id:
        queryset = queryset.filter(models.DBBook.author_id == author_id)

    return queryset.offset(skip).limit(limit).all()
