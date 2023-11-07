from sqlalchemy.orm import Session
from sqlalchemy.orm.strategy_options import joinedload

import models
import schemas


def get_authors(db: Session, offset: int = 0, limit: int = 10):
    return db.query(models.DBAuthor).offset(offset).limit(limit).all()


def get_author(author_id: int, db: Session):
    return (
        db.query(models.DBAuthor).filter(models.DBAuthor.id == author_id).first()
    )


def get_author_by_name(name: str, db: Session):
    return db.query(models.DBAuthor).filter(models.DBAuthor.name == name).first()


def get_author_by_id(author_id: int, db: Session):
    return (
        db.query(models.DBAuthor).filter(models.DBAuthor.id == author_id).first()
    )


def create_author(author: schemas.AuthorCreate, db: Session):
    db_author = models.DBAuthor(**author.model_dump())
    db.add(db_author)
    db.commit()
    db.refresh(db_author)
    return db_author


def get_books(db: Session, offset: int = 0, limit: int = 10):
    return (
        db.query(models.DBBook)
        .offset(offset)
        .limit(limit)
        .options(joinedload(models.DBBook.author))
        .all()
    )


def get_book(book_id: int, db: Session):
    return db.query(models.DBBook).filter(models.DBBook.id == book_id).first()


def create_book(book: schemas.BookCreate, db: Session):
    db_book = models.DBBook(**book.model_dump())
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book
