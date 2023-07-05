from typing import Optional, List

from sqlalchemy.orm import Session
from models import Author, Book
from schemas import AuthorCreate, BookCreate

def create_author(db: Session, author: AuthorCreate) -> Author:
    db_author = Author(name=author.name, bio=author.bio)
    db.add(db_author)
    db.commit()
    db.refresh(db_author)
    return db_author

def get_authors(
    db: Session, skip: int = 0, limit: int = 100
) -> List[Author]:
    return db.query(Author).offset(skip).limit(limit).all()

def get_author(db: Session, author_id: int) -> Optional[Author]:
    return db.query(Author).filter(Author.id == author_id).first()

def create_book(db: Session, book: BookCreate) -> Book:
    db_book = Book(**book.dict())
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book

def get_books(db: Session, skip: int = 0, limit: int = 100) -> List[Book]:
    return db.query(Book).offset(skip).limit(limit).all()

def get_books_by_author(
    db: Session, author_id: int, skip: int = 0, limit: int = 100
) -> List[Book]:
    return (
        db.query(Book).filter(Book.author_id == author_id).
        offset(skip).limit(limit).all()
    )
