from http.client import HTTPException
from sqlalchemy.orm import Session
import schemas
from db import models
from db.models import Author, Book
from schemas import AuthorCreate


def create_author(db: Session, author: AuthorCreate):
    db_author = Author(name=author.name, bio=author.bio)
    db.add(db_author)
    db.commit()
    db.refresh(db_author)
    return db_author


def get_authors(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Author).offset(skip).limit(limit).all()


def get_author(db: Session, author_id: int):
    return db.query(Author).filter(Author.id == author_id).first()


def create_book(db: Session,
                book: schemas.BookCreate,
                author_id: int):
    db_author = (db.query(models.Author).
                 filter(models.Author.id == author_id).first())
    if not db_author:
        raise HTTPException(status_code=404, detail="Author not found")

    db_book = models.Book(
        title=book.title,
        summary=book.summary,
        publication_date=book.publication_date,
        author_id=author_id
    )
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book


def get_books(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Book).offset(skip).limit(limit).all()


def get_books_by_author(db: Session,
                        author_id: int,
                        skip: int = 0,
                        limit: int = 100):
    return (db.query(Book).filter(Book.author_id == author_id).
            offset(skip).limit(limit).all())
