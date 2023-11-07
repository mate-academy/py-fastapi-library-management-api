from fastapi import HTTPException
from sqlalchemy.orm import Session
from datetime import datetime

import models
from models import Author, Book
from schemas import AuthorCreate, BookCreate


def get_all_authors(db: Session):
    return db.query(Author).all()


def create_author(db: Session, author: AuthorCreate):
    db_author = models.Author(name=author.name, bio=author.bio)
    db.add(db_author)
    db.commit()
    db.refresh(db_author)

    return db_author


def get_author(db: Session, author_id: int):
    author = db.query(Author).filter(Author.id == author_id).first()
    if author is None:
        raise HTTPException(status_code=404, detail="Author not found")
    return author


def delete_author(db: Session, author_id: int):
    db_author = get_author(db, author_id)
    if db_author:
        db.delete(db_author)
        db.commit()


def get_all_books(db: Session):
    return db.query(Book).all()


def create_book(db: Session, book: BookCreate):
    current_date = datetime.now().date()
    book.publication_date = current_date
    db_book = Book(**book.model_dump())

    db.add(db_book)
    db.commit()
    db.refresh(db_book)

    return db_book


def get_book(db: Session, book_id: int):
    return db.query(Book).filter(Book.id == book_id).first()


def delete_book(db: Session, book_id: int):
    db_book = get_book(db, book_id)
    if db_book:
        db.delete(db_book)
        db.commit()
