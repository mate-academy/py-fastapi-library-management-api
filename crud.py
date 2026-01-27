from sqlalchemy import select
from sqlalchemy.orm import Session

from models import DBAuthor, DBBook
from schemas import AuthorCreate, BookCreate


def get_author(db: Session, author_id: int):
    stmt = select(DBAuthor).where(DBAuthor.id == author_id)
    return db.execute(stmt).scalar_one_or_none()


def get_author_by_name(db: Session, name: str):
    stmt = select(DBAuthor).where(DBAuthor.name == name)
    return db.execute(stmt).scalar_one_or_none()


def get_authors(db: Session, skip: int = 0, limit: int = 100):
    stmt = select(DBAuthor).offset(skip).limit(limit)
    return db.execute(stmt).scalars().all()


def create_author(db: Session, author: AuthorCreate):
    db_author = DBAuthor(**author.model_dump())

    db.add(db_author)
    db.commit()
    db.refresh(db_author)

    return db_author


def get_book(db: Session, book_id: int):
    stmt = select(DBBook).where(DBBook.id == book_id)
    return db.execute(stmt).scalar_one_or_none()


def get_books(db: Session, skip: int = 0, limit: int = 100):
    """Retrieve a list of books."""
    stmt = select(DBBook).offset(skip).limit(limit)
    return db.execute(stmt).scalars().all()


def create_book(db: Session, book: BookCreate):
    """Create a new book."""
    db_book = DBBook(**book.model_dump())

    db.add(db_book)
    db.commit()
    db.refresh(db_book)

    return db_book


def delete_book(db: Session, book_id: int):
    stmt = select(DBBook).where(DBBook.id == book_id)
    db_book = db.execute(stmt).scalar_one_or_none()

    if db_book:
        db.delete(db_book)
        db.commit()

    return db_book
