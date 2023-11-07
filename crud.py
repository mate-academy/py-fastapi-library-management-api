from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from schemas import AuthorCreate, BookCreate
import models


def get_all_authors(db: Session):
    return db.query(models.Author).all()


def get_author_by_id(db: Session, author_id: int):
    return db.query(models.Author).filter(models.Author.id == author_id).first()


def create_author(db: Session, author: AuthorCreate):
    try:
        db_author = models.Author(name=author.name, bio=author.bio)
        db.add(db_author)
        db.commit()
        db.refresh(db_author)
        return db_author
    except IntegrityError:
        db.rollback()


def get_all_books(db: Session, author_id: int = None):
    if author_id:
        return db.query(models.Book).filter(models.Book.author_id == author_id).all()
    return db.query(models.Book).all()


def get_book_by_id(db: Session, book_id: int):
    return db.query(models.Book).filter(models.Book.id == book_id).first()


def create_book(db: Session, book: BookCreate, author_id: int):
    db_book = models.Book(
        title=book.title,
        summary=book.summary,
        publication_date=book.publication_date,
        author_id=author_id
    )
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book
