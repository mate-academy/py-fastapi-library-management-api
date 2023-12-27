from sqlalchemy import exists

import models
import schemas
from models import Author
from models import Book
from schemas import BookCreate
from sqlalchemy.orm import Session


def create_author(db: Session, author: Author):
    db_author = Author(**author.dict())
    db.add(db_author)
    db.commit()
    db.refresh(db_author)
    return db_author


def get_authors(db: Session, skip: int = 0, limit: int = 10):
    return db.query(Author).offset(skip).limit(limit).all()


def get_author(db: Session, author_id: int):
    return db.query(Author).filter(Author.id == author_id).first()


def check_author_exists(db: Session, author: schemas.AuthorCreate):
    db_author_exists = db.query(exists().where(
        (models.Author.name == author.name) | (models.Author.bio == author.bio)
    )).scalar()

    return db_author_exists


def create_book(db: Session, book: BookCreate, author_id: int):
    db_book = Book(**book.dict(), author_id=author_id)
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book


def get_books(db: Session, skip: int = 0, limit: int = 10):
    return db.query(Book).offset(skip).limit(limit).all()


def get_books_by_author(db: Session, author_id: int, skip: int = 0, limit: int = 10):
    return db.query(Book).filter(Book.author_id == author_id).offset(skip).limit(limit).all()
