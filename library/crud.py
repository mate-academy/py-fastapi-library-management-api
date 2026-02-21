from sqlalchemy.orm import Session
from library.models import Author, Book
from library.schemas import AuthorCreate, BookCreate
from typing import Optional
import sqlalchemy.exc

def create_author(db: Session, author_create: AuthorCreate):
    data = author_create.dict()
    db_author = Author(**data)
    try:
        db.add(db_author)
        db.commit()
        db.refresh(db_author)
    except sqlalchemy.exc.IntegrityError:
        db.rollback()
        raise
    except Exception:
        db.rollback()
    raise


def get_author(db: Session, author_id: int):
    return db.get(Author, author_id)


def get_authors(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Author).order_by(Author.id).offset(skip).limit(limit).all()


def create_book(db: Session, book_create: BookCreate):
    author = db.get(Author, book_create.author_id)
    if author is None:
        return None

    data = book_create.dict()
    db_book = Book(**data)
    try:
        db.add(db_book)
        db.commit()
        db.refresh(db_book)
    except:
        db.rollback()
        raise
    return db_book


def get_book(db: Session, book_id: int):
    return db.get(Book, book_id)


def get_books(db: Session, skip: int = 0, limit: int = 100, author_id: Optional[int] = None):
    q = db.query(Book).order_by(Book.id)
    if author_id is not None:
        q = q.filter(Book.author_id == author_id)
    return q.offset(skip).limit(limit).all()
