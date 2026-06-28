from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from db.models import Author, Book
from schemas import AuthorCreate, BookCreate


def get_all_authors(db: Session, skip: int = 0, limit: int = 10) -> list[Author]:
    return list(db.scalars(select(Author).offset(skip).limit(limit)))


def get_author(db: Session, author_id: int) -> Author | None:
    return db.scalar(select(Author).where(Author.id == author_id))

def get_author_by_name(db: Session, name: str) -> Author | None:
    return db.scalar(select(Author).where(Author.name == name))


def create_author(db: Session, author: AuthorCreate) -> Author:
    existing_author = get_author_by_name(db=db, name=author.name)
    if existing_author:
        raise HTTPException(status_code=400, detail="Author already exists")
    db_author = Author(name=author.name, bio=author.bio)
    db.add(db_author)
    db.commit()
    db.refresh(db_author)
    return db_author


def get_books(
    db: Session,
    skip: int = 0,
    limit: int = 10,
    author_id: int | None = None
) -> list[Book]:
    query = select(Book)

    if author_id is not None:
        query = query.where(Book.author_id == author_id)

    return list(db.scalars(query.offset(skip).limit(limit)))


def get_book(db: Session, book_id: int) -> Book | None:
    return db.scalar(select(Book).where(Book.id == book_id))


def create_book(db: Session, book: BookCreate, author_id: int) -> Book:
    db_book = Book(**book.model_dump(), author_id=author_id)
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book
