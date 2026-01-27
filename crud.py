from sqlalchemy.orm import Session
from typing import List, Optional
from models import Author, Book
import schemas


def create_author(db: Session, author: schemas.AuthorCreate) -> Author:
    db_author = Author(name=author.name, bio=author.bio)
    db.add(db_author)
    db.commit()
    db.refresh(db_author)
    return db_author

def get_author(db: Session, author_id: int) -> Optional[Author]:
    return db.query(Author).filter(Author.id == author_id).first()

def get_authors(db: Session, skip: int = 0, limit: int = 100) -> List[Author]:
    return db.query(Author).offset(skip).limit(limit).all()



def create_book(db: Session, book: schemas.BookCreate) -> Book:
    db_book = Book(
        title=book.title,
        summary=book.summary,
        publication_date=book.publication_date,
        author_id=book.author_id
    )
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book

def get_book(db: Session, book_id: int) -> Optional[Book]:
    return db.query(Book).filter(Book.id == book_id).first()

def get_books(db: Session, skip: int = 0, limit: int = 100, author_id: Optional[int] = None) -> List[Book]:
    query = db.query(Book)
    if author_id is not None:
        query = query.filter(Book.author_id == author_id)
    return query.offset(skip).limit(limit).all()
