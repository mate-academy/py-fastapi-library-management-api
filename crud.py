from typing import Optional

from sqlalchemy.orm import Session

from db.models import DBBook, DBAuthor
from schemas import BookCreate, AuthorCreate


def get_all_books(
        db: Session, author_id: DBAuthor.id | None = None,
        skip: int = 0, limit: int = 100
) -> list[DBBook]:
    queryset = db.query(DBBook)

    if author_id:
        queryset = queryset.filter(DBBook.author_id == author_id)

    return queryset.offset(skip).limit(limit).all()


def get_book_by_book_id(db: Session, book_id: int) -> Optional[DBBook]:
    return db.query(DBBook).filter(DBBook.id == book_id).first()


def create_book(db: Session, book: BookCreate) -> DBBook:
    db_book = DBBook(**book.dict())
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book


def get_all_authors(
        db: Session, skip: int = 0, limit: int = 100
) -> list[DBAuthor]:
    return db.query(DBAuthor).offset(skip).limit(limit).all()


def get_author_by_author_id(
        db: Session, author_id: int
) -> Optional[DBAuthor]:
    return db.query(DBAuthor).filter(
        DBAuthor.id == author_id
    ).first()


def create_author(db: Session, author: AuthorCreate) -> DBAuthor:
    db_author = DBAuthor(name=author.name, bio=author.bio)
    db.add(db_author)
    db.commit()
    db.refresh(db_author)
    return db_author
