from typing import Type


from sqlalchemy.orm import Session

from models import Author, Book
import schemas


def list_pagination(
    db: Session, model: Type[Author] | Type[Book],
        skip: int,
        limit: int
):
    return db.query(model).offset(skip).limit(limit).all()


def create_author(db: Session, author: schemas.AuthorCreate):
    db_author = Author(
        name=author.name,
        bio=author.bio,
    )
    db.add(db_author)
    db.commit()
    db.refresh(db_author)
    return db_author


def list_authors(db: Session, skip: int, limit: int):
    """Retrieve a list of authors with pagination (skip, limit)."""
    return list_pagination(db, Author, skip, limit)


def single_author(db: Session, author_id: int):
    query = db.query(Author).filter(Author.id == author_id).first()
    return query


def create_book(db: Session, book=schemas.BookCreate):
    db_book = Book(
        title=book.title,
        summary=book.summary,
        publication_date=book.publication_date,
        author_id=book.author_id,
    )
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book


def list_books(db: Session, skip: int, limit: int):
    """Retrieve a list of books with pagination (skip, limit)."""
    return list_pagination(db, Book, skip, limit)

def get_books_by_author_id(db: Session, author_id: int):
    db_books = db.query(Book).filter(Book.author_id == author_id).all()
    return db_books