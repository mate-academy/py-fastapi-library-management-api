from sqlalchemy.orm import Session
from typing import List, Optional

from library.models import DBAuthor, DBBook
from library.schemas import AuthorCreate, BookCreate


def get_author_by_name(db: Session, author_name: str) -> Optional[DBAuthor]:
    return db.query(DBAuthor).filter(DBAuthor.name == author_name).first()


def get_author(db: Session, author_id: int) -> Optional[DBAuthor]:
    return db.query(DBAuthor).filter(DBAuthor.id == author_id).first()


def get_authors(db: Session, skip: int = 0, limit: int = 100) -> List[DBAuthor]:
    return db.query(DBAuthor).offset(skip).limit(limit).all()


def create_author(db: Session, author: AuthorCreate) -> DBAuthor:
    db_author = DBAuthor(name=author.name, bio=author.bio)
    db.add(db_author)
    db.commit()
    db.refresh(db_author)
    return db_author


def update_author(db: Session, author_id: int, author: AuthorCreate) -> DBAuthor:
    db_author = get_author(db, author_id)
    db_author.name = author.name
    db_author.bio = author.bio
    db.commit()
    db.refresh(db_author)
    return db_author


def delete_author(db: Session, author_id: int) -> DBAuthor:
    db_author = get_author(db, author_id)
    db.delete(db_author)
    db.commit()
    return db_author


def get_book(db: Session, book_id: int) -> Optional[DBBook]:
    return db.query(DBBook).filter(DBBook.id == book_id).first()


def get_books(db: Session, skip: int = 0, limit: int = 100) -> List[DBBook]:
    return db.query(DBBook).offset(skip).limit(limit).all()


def create_book(db: Session, book: BookCreate) -> DBBook:
    db_book = DBBook(
        title=book.title,
        summary=book.summary,
        publication_date=book.publication_date,
        author_id=book.author_id
    )
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book


def update_book(db: Session, book_id: int, book: BookCreate) -> DBBook:
    db_book = get_book(db, book_id)
    db_book.title = book.title
    db_book.summary = book.summary
    db_book.publication_date = book.publication_date
    db_book.author_id = book.author_id
    db.commit()
    db.refresh(db_book)
    return db_book


def delete_book(db: Session, book_id: int) -> DBBook:
    db_book = get_book(db, book_id)
    db.delete(db_book)
    db.commit()
    return db_book
