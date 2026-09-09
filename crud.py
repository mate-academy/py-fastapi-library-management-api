from sqlalchemy.orm import Session

from db_library import models
import schemas


def create_author(db: Session, author: schemas.AuthorCreate):
    db_author = models.DBAuthor(
        name=author.name,
        bio=author.bio,
    )
    db.add(db_author)
    db.commit()
    db.refresh(db_author)

    return db_author


def get_author_name(db: Session, name: str):
    return db.query(models.DBAuthor).filter(models.DBAuthor.name == name).first()


def get_all_authors(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.DBAuthor).offset(skip).limit(limit).all()


def get_author_by_id(db: Session, author: int):
    return db.query(models.DBAuthor).filter(models.DBAuthor.id == author).first()


def create_book(db: Session, book: schemas.BookCreate):
    db_book = models.DBBook(
        title=book.title, summary=book.summary, author_id=book.author_id
    )
    db.add(db_book)
    db.commit()
    db.refresh(db_book)

    return db_book


def get_all_book_paginate(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.DBBook).offset(skip).limit(limit).all()


def get_book_on_author(db: Session, author: int, skip: int = 0, limit: int = 100):
    return (
        db.query(models.DBBook)
        .filter(models.DBBook.author_id == author)
        .offset(skip)
        .limit(limit)
        .all()
    )
