from typing import Optional

from sqlalchemy.orm import Session

from models import DBAuthors, DBBooks
from schemas import AuthorsCreate, BookCreate


def get_all_authors(db: Session, skip: int, limit: int) -> Optional[list]:
    return db.query(DBAuthors).offset(skip).limit(limit).all()


def create_author_crud(db: Session, author: AuthorsCreate) -> DBAuthors:
    db_author = DBAuthors(name=author.name, bio=author.bio)
    db.add(db_author)
    db.commit()
    db.refresh(db_author)
    return db_author


def get_author_by_name(db: Session, name: str) -> Optional[DBAuthors]:
    return db.query(DBAuthors).filter(DBAuthors.name == name).first()


def get_author_by_id_crud(db: Session, author_id: int) -> Optional[DBAuthors]:
    return db.query(DBAuthors).filter(DBAuthors.id == author_id).first()


def get_all_books(
        db: Session,
        skip: int,
        limit: int,
        author_id: Optional[int] = None
) -> list:
    queryset = db.query(DBBooks)

    if author_id:
        queryset = queryset.filter(DBBooks.author_id == author_id)

    return queryset.offset(skip).limit(limit).all()


def create_book_crud(db: Session, book: BookCreate) -> DBBooks:
    db_book = DBBooks(
        title=book.title,
        summary=book.summary,
        publication_date=book.publication_date,
        author_id=book.author_id
    )
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book
