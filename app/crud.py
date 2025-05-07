from sqlalchemy.orm import Session
from models import Author, Book
import schemas

def create_author(db: Session, author: schemas.AuthorCreate) -> Author:
    db_author = Author(**author.dict())
    db.add(db_author)
    db.commit()
    db.refresh(db_author)
    return db_author

def get_authors(db: Session, skip: int = 0, limit: int = 10):
    return db.query(Author).offset(skip).limit(limit).all()

def get_author(db: Session, author_id: int):
    return db.query(Author).filter(Author.id == author_id).first()

def create_book(db: Session, book: schemas.BookCreate, author_id: int) -> Book:
    db_book = Book(**book.dict(), author_id=author_id)
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book

def get_books(db: Session, skip: int = 0, limit: int = 10):
    return db.query(Book).offset(skip).limit(limit).all()

def get_books_by_author(db: Session, author_id: int):
    return db.query(Book).filter(Book.author_id == author_id).all()