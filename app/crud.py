from sqlalchemy.orm import Session
from . import models, schemas

def create_author(db: Session, author: schemas.AuthorCreate) -> models.Author:
    new_author = models.Author(name=author.name, bio=author.bio)
    db.add(new_author)
    db.commit()
    db.refresh(new_author)
    return new_author

def create_book(db: Session, book: schemas.BookCreate, author_id: int) -> models.Book:
    new_book = models.Book(**book.dict(), author_id=author_id)
    db.add(new_book)
    db.commit()
    db.refresh(new_book)
    return new_book

def get_book(db: Session, book_id: int) -> models.Book:
    return db.query(models.Book).filter(models.Book.id == book_id).first()

def get_author(db: Session, author_id: int) -> models.Author:
    return db.query(models.Author).filter(models.Author.id == author_id).first()

def get_books_by_author(db: Session, author_id: int) -> list[models.Book]:
    return db.query(models.Book).filter(models.Book.author_id == author_id).all()
