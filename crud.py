from typing import Type, Optional

from sqlalchemy.orm import Session, joinedload

from models import Author, Book
from schemas import AuthorCreate, BookCreate, AuthorUpdate, BookUpdate


def create_author(db: Session, author: AuthorCreate) -> Author:
    db_author = Author(name=author.name, bio=author.bio)
    db.add(db_author)
    db.commit()
    db.refresh(db_author)
    return db_author


def get_authors(db: Session, skip: int = 0, limit: int = 100) -> list[Type[Author]]:
    return db.query(Author).offset(skip).limit(limit).all()


def get_author(db: Session, author_id: int) -> Optional[Author]:
    return db.query(Author).filter(Author.id == author_id).first()


def update_author(
    db: Session, author_id: int, author: AuthorUpdate
) -> Type[Author] | None:
    db_author = db.query(Author).filter(Author.id == author_id).first()
    if db_author is None:
        return None
    for field, value in vars(author).items():
        setattr(db_author, field, value) if value else None
    db.add(db_author)
    db.commit()
    db.refresh(db_author)
    return db_author


def delete_author(db: Session, author_id: int) -> Type[Author] | None:
    db_author = db.query(Author).filter(Author.id == author_id).first()
    if db_author is None:
        return None
    db.delete(db_author)
    db.commit()
    return db_author


def create_book(db: Session, book: BookCreate) -> Book:
    db_book = Book(**book.dict())
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book


def create_book_for_author(db: Session, book: BookCreate, author_id: int) -> Book:
    db_book = Book(**book.dict(), author_id=author_id)
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book


def get_books(db: Session, skip: int = 0, limit: int = 100) -> list[Type[Book]]:
    return db.query(Book).offset(skip).limit(limit).all()


def get_books_by_author(
    db: Session, author_id: int, skip: int = 0, limit: int = 100
) -> list[Type[Book]]:
    return (
        db.query(Book)
        .filter(Book.author_id == author_id)
        .offset(skip)
        .limit(limit)
        .all()
    )


def get_book(db: Session, book_id: int) -> Optional[Book]:
    return (
        db.query(Book)
        .options(joinedload(Book.author))
        .filter(Book.id == book_id)
        .first()
    )


def update_book(db: Session, book_id: int, book: BookUpdate) -> Type[Book] | None:
    db_book = db.query(Book).filter(Book.id == book_id).first()
    if db_book is None:
        return None
    for field, value in vars(book).items():
        setattr(db_book, field, value) if value else None
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book


def delete_book(db: Session, book_id: int) -> Type[Book] | None:
    db_book = db.query(Book).filter(Book.id == book_id).first()
    if db_book:
        db.delete(db_book)
        db.commit()
        return db_book
    else:
        return None
