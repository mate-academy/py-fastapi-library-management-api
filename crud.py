from sqlalchemy.orm import Session
from typing import List, Optional
from models import Author, Book
from schemas import AuthorCreate, BookCreate


def get_authors(db: Session) -> List[Author]:
    return db.query(Author).all()


def get_author(db: Session, author_id: int) -> Optional[Author]:
    return db.query(Author).filter(Author.id == author_id).first()


def get_author_by_name(db: Session, name: str) -> Optional[Author]:
    return db.query(Author).filter(Author.name == name).first()


def create_author(db: Session, author: AuthorCreate) -> Author:
    db_author = Author(name=author.name, bio=author.bio)
    db.add(db_author)
    db.commit()
    db.refresh(db_author)
    return db_author


def delete_author(db: Session, author_id: int) -> Optional[Author]:
    author = get_author(db, author_id)
    if author:
        db.delete(author)
        db.commit()
    return author


def get_books(db: Session) -> List[Book]:
    return db.query(Book).all()


def get_book(db: Session, book_id: int) -> Optional[Book]:
    return db.query(Book).filter(Book.id == book_id).first()


def create_book(db: Session, book: BookCreate) -> Book:
    db_book = Book(
        title=book.title,
        summary=book.summary,
        publication_date=book.publication_date,
        author_id=book.author_id
    )
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book


def delete_book(db: Session, book_id: int) -> Optional[Book]:
    book = get_book(db, book_id)
    if book:
        db.delete(book)
        db.commit()
    return book
