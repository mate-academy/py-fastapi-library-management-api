from sqlalchemy.orm import Session

from app.models import Author, Book
from app.schemas import AuthorCreate, BookCreate


def get_author(db: Session, author_id: int):
    return db.query(Author).filter(Author.id == author_id).first()


def get_authors(db: Session, skip: int = 0, limit: int = 10):
    return db.query(Author).offset(skip).limit(limit).all()


def create_author(db: Session, author: AuthorCreate):
    db_author = Author(name=author.name, bio=author.bio)
    db.add(db_author)
    db.commit()
    db.refresh(db_author)
    return db_author


def get_books(db: Session, skip: int = 0, limit: int = 10):
    return db.query(Book).offset(skip).limit(limit).all()


def create_book(db: Session, book: BookCreate, author_id: int):
    db_book = Book(**book.model_dump, author_id=author_id)
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book
