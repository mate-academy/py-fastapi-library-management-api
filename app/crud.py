from typing import Optional

from sqlalchemy.orm import Session

from app.models import DBAuthor, DBBook
from app.schemas import AuthorsCreate, BookCreate


def get_all_authors(db: Session, skip: int, limit: int) -> Optional[list]:
    return db.query(DBAuthor).offset(skip).limit(limit).all()


def create_author_crud(db: Session, author: AuthorsCreate) -> DBAuthor:
    db_author = DBAuthor(name=author.name, bio=author.bio)
    db.add(db_author)
    db.commit()
    db.refresh(db_author)
    return db_author


def get_author_by_name(db: Session, name: str) -> Optional[DBAuthor]:
    return db.query(DBAuthor).filter(DBAuthor.name == name).first()


def get_author_by_id_crud(db: Session, author_id: int) -> Optional[DBAuthor]:
    return db.query(DBAuthor).filter(DBAuthor.id == author_id).first()


def get_all_books(
        db: Session,
        skip: int,
        limit: int,
        author_id: Optional[int] = None
) -> list:
    queryset = db.query(DBBook)

    if author_id:
        queryset = queryset.filter(DBBook.author_id == author_id)

    return queryset.offset(skip).limit(limit).all()


def create_book_crud(db: Session, book: BookCreate) -> DBBook:
    db_book = DBBook(
        title=book.title,
        summary=book.summary,
        publication_date=book.publication_date,
        author_id=book.author_id
    )
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book
