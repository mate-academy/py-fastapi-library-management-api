from sqlalchemy import select
from sqlalchemy.orm import Session

from models import Author, Book


def get_all_authors(db: Session, skip, limit):
    stmt = select(Author).offset(skip).limit(limit)
    return db.scalars(stmt).all()


def create_author(db: Session, data):
    author = Author(name=data.name, bio=data.bio)
    db.add(author)
    db.commit()
    db.refresh(author)
    return author


def get_single_author(db: Session, author_id: int):
    stmt = select(Author).where(Author.id == author_id)
    return db.scalar(stmt)


def create_book(db: Session, data):
    book = Book(title=data.title,
                summary=data.summary,
                publication_date=data.publication_date,
                author_id=data.author_id)
    db.add(book)
    db.commit()
    db.refresh(book)
    return book


def get_all_books(db: Session, skip, limit):
    stmt = select(Book).offset(skip).limit(limit)
    return db.scalars(stmt).all()


def filter_book(db: Session, author_id, skip, limit):
    stmt = select(Book).where(Book.author_id == author_id).offset(skip).limit(limit)
    return db.scalars(stmt).all()