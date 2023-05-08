from typing import List, Optional

from sqlalchemy.orm import Session
from database.models import DBAuthor, DBBook
from schemas import AuthorCreate, AuthorUpdate, BookCreate, BookUpdate


def create_author(db: Session, author: AuthorCreate) -> DBAuthor:
    db_author = DBAuthor(name=author.name, bio=author.bio)
    db.add(db_author)
    db.commit()
    db.refresh(db_author)
    return db_author


def get_authors(db: Session, skip: int = 0, limit: int = 100) -> List[DBAuthor]:
    return db.query(DBAuthor).offset(skip).limit(limit).all()


def get_author(db: Session, author_id: int) -> Optional[DBAuthor]:
    return db.query(DBAuthor).filter(DBAuthor.id == author_id).first()


def update_author(db: Session, author: DBAuthor, updates: AuthorUpdate) -> DBAuthor:
    for field, value in updates.dict().items():
        setattr(author, field, value)
    db.commit()
    db.refresh(author)
    return author


def delete_author(db: Session, author: DBAuthor):
    db.delete(author)
    db.commit()


def create_book(db: Session, book: BookCreate, author_id: int) -> DBBook:
    db_book = DBBook(**book.dict(), author_id=author_id)
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book


def get_books(db: Session, skip: int = 0, limit: int = 100) -> List[DBBook]:
    return db.query(DBBook).offset(skip).limit(limit).all()


def get_books_by_author(db: Session, author_id: int, skip: int = 0, limit: int = 100) -> List[DBBook]:
    return db.query(DBBook).filter(DBBook.author_id == author_id).offset(skip).limit(limit).all()


def get_book(db: Session, book_id: int) -> Optional[DBBook]:
    return db.query(DBBook).filter(DBBook.id == book_id).first()


def update_book(db: Session, book: DBBook, updates: BookUpdate) -> DBBook:
    for field, value in updates.dict().items():
        setattr(book, field, value)
    db.commit()
    db.refresh(book)
    return book


def delete_book(db: Session, book: DBBook):
    db.delete(book)
    db.commit()
