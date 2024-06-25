from sqlalchemy.orm import Session

from db.models import DBAuthor, DBBook
from schemas import AuthorCreate, BookCreate


def get_author_by_name(db: Session, name: str):
    return db.query(DBAuthor).filter(DBAuthor.name == name).first()


def get_authors_with_pagination(db: Session, skip: int = 0, limit: int = 10):
    return db.query(DBAuthor).offset(skip).limit(limit).all()


def get_author_by_id(db: Session, author_id: int):
    return db.query(DBAuthor).filter(DBAuthor.id == author_id).first()


def create_author(db: Session, author: AuthorCreate):
    db_author = DBAuthor(
        name=author.name,
        bio=author.bio,
    )
    db.add(db_author)
    db.commit()
    db.refresh(db_author)
    return db_author


def get_books_with_pagination(db: Session, skip: int = 0, limit: int = 10):
    return db.query(DBBook).offset(skip).limit(limit).all()


def get_books_by_author(db: Session, author_id: int):
    return db.query(DBBook).filter(DBBook.author_id == author_id)


def create_book(db: Session, book: BookCreate):
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
