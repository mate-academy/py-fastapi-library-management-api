from sqlalchemy.orm import Session
from sqlalchemy import select

import schemas
from models import Book, Author
from schemas import BooksCreate


def get_all_books(db: Session, skip: int = 0, limit: int = 100, author_id: int| None = None):
    query = select(Book)
    if author_id is not None:
        query = query.where(Book.author_id == author_id)

    return db.scalars(query.offset(skip).limit(limit)).all()


def create_book(db: Session, book: BooksCreate):
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


def get_all_author(db: Session, skip: int = 0, limit: int = 100):
    return db.scalars(select(Author).offset(skip).limit(limit)).all()

def get_author(db: Session, author_id: int):
    return db.scalars(select(Author).where(Author.id == author_id)).first()


def create_author(db: Session, author: schemas.AuthorCreate):
    db_author = Author(
        name=author.name,
        bio=author.bio
    )
    db.add(db_author)
    db.commit()
    db.refresh(db_author)
    return db_author
