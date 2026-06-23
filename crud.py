from sqlalchemy import select
from sqlalchemy.orm import Session
import models
import schemas


def get_author(db: Session, author_id: int):
    query = select(models.Author).where(models.Author.id == author_id)
    return db.scalar(query)


def get_authors(db: Session, skip: int = 0, limit: int = 100):
    query = select(models.Author).offset(skip).limit(limit)
    return db.scalars(query).all()


def create_author(db: Session, author: schemas.AuthorCreate):
    db_author = models.Author(name=author.name, bio=author.bio)
    db.add(db_author)
    db.commit()
    db.refresh(db_author)
    return db_author


def get_books(db: Session, skip: int = 0, limit: int = 100):
    query = select(models.Book).offset(skip).limit(limit)
    return db.scalars(query).all()


def get_books_by_author(db: Session, author_id: int):
    query = select(models.Book).where(models.Book.author_id == author_id)
    return db.scalars(query).all()


def create_book(db: Session, book: schemas.BookCreate, author_id: int):
    db_book = models.Book(**book.model_dump(), author_id=author_id)
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book
