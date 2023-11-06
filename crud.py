from sqlalchemy.orm import Session

from db import models
from db.models import DBAuthor, DBBook
from schemas import AuthorCreate, BookCreate


def create_author(db: Session, author: AuthorCreate):
    db_author = DBAuthor(
        name=author.name,
        bio=author.bio,
    )
    db.add(db_author)
    db.commit()
    db.refresh(db_author)

    return db_author


def create_book(db: Session, book: BookCreate):
    db_book = DBBook(
        title=book.title,
        summary=book.summary,
        publication_date=book.publication_date,
        author_id=book.author_id,
    )
    db.add(db_book)
    db.commit()
    db.refresh(db_book)

    return db_book


def get_all_authors(db: Session, skip: int = 0, limit: int = 10):
    return db.query(DBAuthor).offset(skip).limit(limit).all()


def get_all_books(
        db: Session,
        author_id: int = None,
        skip: int = 0,
        limit: int = 100
):
    queryset = db.query(models.DBBook)

    if author_id is not None:
        queryset = queryset.filter(models.DBBook.authors_id == author_id)

    return queryset.offset(skip).limit(limit).all()


def get_book_by_id(db: Session, book_id: int):
    return db.query(DBBook).get(DBBook.id == book_id)


def get_author_by_id(db: Session, author_id: int):
    return db.query(DBAuthor).filter(DBAuthor.id == author_id).first()


def get_books_by_author(db: Session, author_id: int):
    return db.query(DBBook).filter(DBBook.author_id == author_id).all()

