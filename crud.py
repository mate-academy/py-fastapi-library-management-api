from sqlalchemy.orm import Session

from models import Author, Book
from schemas import (
    AuthorCreate,
    BookCreate,
    BookCreateForAuthor
)


def get_all_authors_with_pagination(
        db: Session,
        skip: int = 0,
        limit: int = 100
):
    return db.query(Author).offset(skip).limit(limit).all()


def get_author_by_id(db: Session, author_id: int):
    return db.query(Author).filter(Author.id == author_id).first()


def get_author_by_name(db: Session, author_name: str):
    return db.query(Author).filter(
        Author.name == author_name
    ).first()


def create_author(db: Session, author: AuthorCreate):
    db_author = Author(**author.dict())
    db.add(db_author)
    db.commit()
    db.refresh(db_author)
    return db_author


def create_book_for_author(
        db: Session,
        book: BookCreateForAuthor,
        author_id: int
):
    db_book = Book(**book.dict(), author_id=author_id)
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book


def create_book(db: Session, book: BookCreate):
    db_book = Book(**book.dict())
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book


def get_all_books_with_pagination(
        db: Session,
        skip: int = 0,
        limit: int = 100,
        author_id=None
):
    if author_id:
        return db.query(Book).filter(
            Book.author_id == author_id
        ).offset(skip).limit(limit).all()
    return db.query(Book).offset(skip).limit(limit).all()
