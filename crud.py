from sqlalchemy import select
from sqlalchemy.orm import Session

import schemas
from models import Author, Book


def get_all_authors(db: Session, skip: int = 0, limit: int = 10):
    return db.scalars(select(Author).offset(skip).limit(limit)).all()


def create_author(db: Session, author: schemas.AuthorCreate):
    db_author = Author(name=author.name, bio=author.bio)
    db.add(db_author)
    db.commit()
    db.refresh(db_author)
    return db_author


def get_author_by_id(db: Session, author_id: int):
    return db.scalar(select(Author).where(Author.id == author_id))


def get_all_books(db: Session, skip: int = 0, limit: int = 10):
    return db.scalars(select(Book).offset(skip).limit(limit)).all()


def create_book(db: Session, book: schemas.BookCreate):
    db_book = Book(
        title=book.title,
        summary=book.summary,
        publication_date=book.publication_date,
        author_id=book.author_id,
    )
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book


def get_books_by_author_id(db: Session, author_id: int):
    return db.query(Book).filter(Book.author_id == author_id).all()
