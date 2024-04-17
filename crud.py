from sqlalchemy.orm import Session

from db.models import DBBook, DBAuthor
import schemas


def create_author(db: Session, author: schemas.AuthorCreate):
    db_author = DBAuthor(**author.dict())
    db.add(db_author)
    db.commit()
    db.refresh(db_author)
    return db_author


def get_authors(db: Session, skip: int = 0, limit: int = 10):
    return db.query(DBAuthor).offset(skip).limit(limit).all()


def get_author(db: Session, author_id: int):
    return db.query(DBAuthor).filter(DBAuthor.id == author_id).first()


def create_book(db: Session, book: schemas.BookCreate):
    db_book = DBBook(**book.dict())
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book


def get_books(db: Session, skip: int = 0, limit: int = 10):
    return db.query(DBBook).offset(skip).limit(limit).all()


def get_books_by_author(
        db: Session, author_id: int
):
    return db.query(DBBook).filter(DBBook.author_id == author_id)
