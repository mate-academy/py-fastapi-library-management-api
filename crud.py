from sqlalchemy.orm import Session
from db import models
import schemas

def get_authors(db: Session, skip: int, limit: int):
    return db.query(models.DBAuthor).offset(skip).limit(limit).all()


def create_author(db: Session, author: schemas.CreateAuthor):
    db_author = models.DBAuthor(
        name = author.name,
        bio = author.bio
    )
    db.add(db_author)
    db.commit()
    db.refresh(db_author)
    return db_author


def get_author_by_id(db: Session, author_id: int):
    return db.query(models.DBAuthor).filter(models.DBAuthor.id == author_id).first()


def get_books(db: Session, skip: int, limit: int):
    return db.query(models.DBBook).offset(skip).limit(limit).all()


def create_book(db: Session, book: schemas.CreateBook):
    db_book = models.DBBook(
        title = book.title,
        summary = book.summary,
        publication_date = book.publication_date,
        author_id = book.author_id
    )
    author = db.query(models.DBAuthor).filter(models.DBAuthor.id == book.author_id).first()
    if not author:
        raise ValueError("Author not found")
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book


def get_book_by_author_id(db: Session, author_id: int, skip: int, limit: int):
    return db.query(models.DBBook).filter(models.DBBook.author_id == author_id).offset(skip).limit(limit).all()
