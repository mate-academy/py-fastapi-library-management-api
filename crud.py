from sqlalchemy.orm import Session

import models
import schemas


def get_authors(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.DBAuthor).offset(skip).limit(limit).all()


def get_author(db: Session, author_id: int):
    return db.query(models.DBAuthor).filter(models.DBAuthor.id == author_id).first()


def get_author_by_name(db: Session, name: str):
    return db.query(models.DBAuthor).filter(models.DBAuthor.name == name).first()


def create_author(db: Session, author: schemas.AuthorCreate):
    db_author = models.DBAuthor(**author.dict())
    db.add(db_author)
    db.commit()
    db.refresh(db_author)

    return db_author


def get_books(
    db: Session, skip: int = 0, limit: int = 100, author_id: int | None = None
):
    queryset = db.query(models.DBBook)
    if author_id:
        queryset = queryset.filter(models.DBBook.author_id == author_id)
    queryset = queryset.offset(skip).limit(limit)
    return queryset.all()


def get_book(db: Session, book_id: int):
    return db.query(models.DBBook).filter(models.DBBook.id == book_id).first()


def create_book(db: Session, book: schemas.BookCreate):
    db_book = models.DBBook(**book.dict())
    db.add(db_book)
    db.commit()
    db.refresh(db_book)

    return db_book
