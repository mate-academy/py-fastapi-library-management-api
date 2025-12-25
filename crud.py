from sqlalchemy import select
from sqlalchemy.orm import Session

from models import Author, Book
from schemas import AuthorCreate, BookCreate


def get_authors_list(db: Session,
                     skip: int = 0,
                     limit: int = 100
                     ):
    return db.scalars(
        select(Author).offset(skip).limit(limit)
    ).all()


def get_author_by_id(db: Session, author_id: int):
    return db.scalars(
        select(Author).where(
            Author.id == author_id)
    ).first()


def create_author(db: Session, author: AuthorCreate):
    db_author = Author(**author.model_dump())

    db.add(db_author)
    db.commit()
    db.refresh(db_author)

    return db_author


def get_books_list(db: Session,
                   author_id: int | None = None,
                   skip: int = 0,
                   limit: int = 100
                   ):
    qs = select(Book)
    if author_id is not None:
        qs = qs.where(Book.author_id == author_id)

    return db.scalars(qs.offset(skip).limit(limit)).all()


def get_book_by_id(db: Session, book_id: int):
    return db.scalars(select(Book).where(Book.id == book_id)).first()


def create_book(db: Session, book: BookCreate):
    db_book = Book(**book.model_dump())

    db.add(db_book)
    db.commit()
    db.refresh(db_book)

    return db_book
