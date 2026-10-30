from sqlalchemy import select
from sqlalchemy.orm import Session
from models import Author, Book
from schemas import AuthorCreate, BookCreate

def get_author(db: Session, author_id: int) -> Author | None:
    return db.get(Author, author_id)

def get_authors(db: Session, skip: int = 0, limit: int = 100) -> list[Author]:
    stmt = select(Author).offset(skip).limit(limit)
    return list(db.scalars(stmt).all())

def create_author(db: Session, author: AuthorCreate) -> Author:
    db_author = Author(name=author.name, bio=author.bio)
    db.add(db_author)
    db.commit()
    db.refresh(db_author)
    return db_author


def get_books(db: Session, skip: int = 0, limit: int = 100, author_id: int | None = None) -> list[Book]:
    stmt = select(Book)
    if author_id is not None:
        stmt = stmt.where(Book.author_id == author_id)
    stmt = stmt.offset(skip).limit(limit)
    return list(db.scalars(stmt).all())

def create_book(db: Session, book: BookCreate, author_id: int) -> Book:
    db_book = Book(**book.model_dump(), author_id=author_id)
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book
