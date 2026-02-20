import sqlalchemy
from fastapi import HTTPException
from sqlalchemy.orm import Session

from db import models
import schemas


def get_all_authors(db: Session, skip: int = 0, limit: int = None):
    return db.query(models.Author).offset(skip).limit(limit).all()


def get_author(db: Session, author_id: int):
    author = (
        db.query(
            models.Author
        ).filter(
            models.Author.id == author_id
        ).first()
    )
    return author


def get_author_by_name(db: Session, author_name: str):
    db_author = (
        db.query(
            models.Author
        ).filter(
            models.Author.name == author_name
        ).first()
    )
    return db_author



def create_author(db: Session, author: schemas.AuthorCreate):
    db_author = models.Author(name=author.name, bio=author.bio)
    db.add(db_author)

    try:
        db.commit()
    except (sqlalchemy.exc.IntegrityError, sqlalchemy.exc.SQLAlchemyError):
        db.rollback()
        raise HTTPException(status_code=400, detail="Book already exists")

    db.refresh(db_author)
    return db_author

def get_all_books(db: Session, skip: int = 0, limit: int = None):
    return db.query(models.Book).offset(skip).limit(limit).all()


def get_books_by_author_id(db: Session, author_id: int, skip: int = 0, limit: int = None):
    return (
        db.query(
            models.Book
        ).filter(
            models.Book.author_id == author_id
        ).offset(skip).limit(limit).all()
    )

def create_book(db: Session, book: schemas.BookCreate):
    db_book = models.Book(title=book.title,
                          summary=book.summary,
                          publication_date=book.publication_date,
                          author_id=book.author_id)

    db.add(db_book)
    try:
        db.commit()
    except (sqlalchemy.exc.IntegrityError, sqlalchemy.exc.SQLAlchemyError):
        db.rollback()
        raise HTTPException(status_code=400, detail="Book already exists")

    db.refresh(db_book)
    return db_book