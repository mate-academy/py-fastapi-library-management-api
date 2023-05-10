from sqlalchemy.orm import Session
from db import models
import schemas
from db.models import Author, Book


def get_all_books(db: Session, skip: int = 0, limit: int = 100) -> list[Book]:
    return db.query(models.Book).offset(skip).limit(limit).all()


def get_book(db: Session, book_id: int) -> Book:
    return db.query(models.Book).filter(
        models.Book.id == book_id
    ).first()


def filter_books_by_author(db: Session, author_id: int) -> list[Books]:
    return db.query(models.Book).filter(
        models.Book.author_id == author_id).all()


def create_book(db: Session, book: schemas.BookCreate) -> Book:
    db_book = models.Book(
        title=book.title,
        summary=book.summary,
        publication_date=book.publication_date,
        author_id=book.author_id
    )
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book


def get_all_authors(db: Session, skip: int = 0, limit: int = 50) -> list[Author]:
    return db.query(models.Author).offset(skip).limit(limit).all()


def get_author(db: Session, author_id: int) -> Author:
    return db.query(models.Author).filter(
        models.Author.id == author_id
    ).first()


def create_author(db: Session, author: schemas.AuthorCreate) -> Author:
    db_author = models.Book(
        name=author.name,
        bio=author.bio,
    )
    db.add(db_author)
    db.commit()
    db.refresh(db_author)
    return db_author
