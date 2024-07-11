from datetime import date
from typing import List

from sqlalchemy.orm import Session

from db.models import DBAuthor, DBBook


def get_all_authors(
        db: Session,
        skip: int = 0,
        limit: int = 100
) -> List[DBAuthor]:
    return db.query(DBAuthor).offset(skip).limit(limit).all()


def get_single_author(db: Session, author_id: int) -> DBAuthor:
    return db.query(DBAuthor).filter(DBAuthor.id == author_id).first()


def create_author(db: Session, name: str, bio: str) -> DBAuthor:
    new_author = DBAuthor(name=name, bio=bio)
    db.add(new_author)
    db.commit()
    db.refresh(new_author)
    return new_author


def get_all_books(
        db: Session,
        skip: int = 0,
        limit: int = 100
) -> List[DBBook]:
    return db.query(DBBook).offset(skip).limit(limit).all()


def get_books_by_author_id(db: Session, author_id: int) -> List[DBBook]:
    return db.query(DBBook).filter(DBBook.author_id == author_id).all()


def create_book(
        db: Session,
        title: str,
        summary: str,
        publication_date: date,
        author_id: int
) -> DBBook:
    new_book = DBBook(
        title=title,
        summary=summary,
        publication_date=publication_date,
        author_id=author_id
    )
    db.add(new_book)
    db.commit()
    db.refresh(new_book)
    return new_book
