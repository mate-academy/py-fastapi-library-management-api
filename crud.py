from sqlalchemy import select
from sqlalchemy.orm import Session

import schemas
from models import Author, Book


def get_authors(db: Session, skip: int = 0, limit: int = 100):
    stmt = select(Author).offset(skip).limit(limit)
    result = db.execute(stmt)
    return result.scalars().all()


def get_author_by_name(db: Session, name: str):
    stmt = select(Author).where(Author.name == name)
    result = db.execute(stmt)
    return result.scalar_one_or_none()


def create_author(db: Session, author: schemas.AuthorCreate):
    db_author = Author(name=author.name, bio=author.bio)
    db.add(db_author)
    db.commit()
    db.refresh(db_author)
    return db_author


def get_author_by_id(db: Session, author_id: int):
    stmt = select(Author).where(Author.id == author_id)
    result = db.execute(stmt)
    return result.scalar_one_or_none()


def create_book_for_author(
    db: Session, book: schemas.BookCreate, author_id: int
):
    db_book = Book(
        title=book.title,
        summary=book.summary,
        publication_date=book.publication_date,
        author_id=author_id,
    )
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book


def get_books_for_author(db: Session, author_id: int):
    stmt = select(Book).where(Book.author_id == author_id)
    result = db.execute(stmt)
    return result.scalars().all()


def get_books(db: Session, skip: int = 0, limit: int = 100):
    stmt = select(Book).offset(skip).limit(limit)
    result = db.execute(stmt)
    return result.scalars().all()
