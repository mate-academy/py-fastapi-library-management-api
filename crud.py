from sqlalchemy.orm import Session

from db.models import Author, Book
from schemas import AuthorCreate, BookCreate


def create_author(db: Session, author: AuthorCreate):
    db_author = Author(**author.model_dump())
    db.add(db_author)
    db.commit()
    db.refresh(db_author)

    return db_author


def create_book(db: Session, book: BookCreate):
    db_book = Book(**book.model_dump())
    db.add(db_book)
    db.commit()
    db.refresh(db_book)

    return db_book


def get_authors(db: Session, skip: int = 0, limit: int = 10):
    return db.query(Author).offset(skip).limit(limit).all()


def get_author_by_id(db: Session, author_id: int):
    return db.query(Author).filter(Author.id == author_id).first()


def get_books(db: Session, skip: int = 0, limit: int = 10):
    return db.query(Book).offset(skip).limit(limit).all()


def get_books_by_author(db: Session, author_id: int):
    return db.query(Book).filter(Book.author_id == author_id).all()
