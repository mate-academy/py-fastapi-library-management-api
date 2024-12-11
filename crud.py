from sqlalchemy.orm import Session

import models
from schemas import AuthorCreate, BookCreate


def get_all_authors(
        db: Session,
        skip: int = 0,
        limit: int = 5,
):
    """
       Retrieve a list of authors with pagination.
    """
    return db.query(models.DBAuthor).offset(skip).limit(limit).all()


def get_author_by_id(db: Session, author_id: int):
    """
       Retrieve a single author by ID.
    """
    return (
        db.query(models.DBAuthor).
        filter(models.DBAuthor.id == author_id).first()
    )


def get_author_by_name(db: Session, name: str):
    return (
        db.query(models.DBAuthor).filter(models.DBAuthor.name == name).first()
    )


def create_author(db: Session, author: AuthorCreate):
    """Creates a new author to the database."""
    db_author = models.DBAuthor(
        name=author.name,
        bio=author.bio,
    )
    db.add(db_author)
    db.commit()
    db.refresh(db_author)

    return db_author


def get_all_books(
        db: Session,
        skip: int = 0,
        limit: int = 5,
        author_id: int = None,
):
    """
    Returns all books in the database with
    optional pagination and filtering by author_id.
    """
    query = db.query(models.DBBook)
    if author_id:
        query = query.filter(models.DBBook.author_id == author_id)
    books = query.offset(skip).limit(limit).all()
    return books


def get_book_by_name(db: Session, title: str):
    return (
        db.query(models.DBBook).filter(models.DBBook.title == title).first()
    )


def create_book(db: Session, book: BookCreate):
    """Creates a new book, connected to the author."""

    db_book = models.DBBook(
        title=book.title,
        summary=book.summary,
        publication_date=book.publication_date,
        author_id=book.author_id,
    )
    db.add(db_book)
    db.commit()
    db.refresh(db_book)

    return db_book
