from sqlalchemy.orm import Session

import models
import schemas
from models import Author

def create_author(db: Session, author: schemas.AuthorCreate):
    db_author = models.Author(name=author.name,bio=author.bio)
    db.add(db_author)
    db.commit()
    db.refresh(db_author)
    return db_author

def get_authors(db: Session, skip: int = 0, limit: int = 10):
    return db.query(Author).offset(skip).limit(limit).all()

def get_author_by_id(db: Session, author_id: int):
    return db.query(Author).filter(Author.id == author_id).first()

def create_new_book_for_author(db: Session, book: schemas.BookCreate):
    db_book = models.Book(title=book.title,summary=book.summary,publication_data=book.publication_data,author_id=book.author_id)
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book

def get_books(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.Book).offset(skip).limit(limit).all()

def get_book_by_id(db: Session, author_id: int):
    return db.query(models.Book).filter(models.Book.id == author_id).first()
