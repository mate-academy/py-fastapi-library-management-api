from sqlalchemy.orm import Session
from db.models import Author, Book
from schemas import (AuthorCreate,
                     AuthorUpdate,
                     BookCreate)


def create_author(
        db: Session,
        author: AuthorCreate
):
    db_author = Author(
        name=author.name,
        bio=author.bio
    )
    db.add(db_author)
    db.commit()
    db.refresh(db_author)
    return db_author


def update_author(
        db: Session,
        author: AuthorUpdate,
        author_id: int
):
    db_author = db.query(Author).get(Author.id == author_id)
    db_author.name = author.name
    db_author.bio = author.bio
    db.add(db_author)
    db.commit()
    db.refresh(db_author)
    return db_author


def get_author_by_id(
        db: Session,
        author_id: int
):
    return db.query(Author).get(Author.id == author_id)


def get_author_list(
        db: Session,
        skip: int = 0,
        limit: int = 5
):
    return db.query(Author).offset(skip).limit(limit).all()


def get_book_by_author_id(
        db: Session,
        author_id: int
):
    return db.query(Book).filter(Book.author_id == author_id)


def get_book_list(
        db: Session,
        skip: int = 0,
        limit: int = 5
):
    return db.query(Book).offset(skip).limit(limit).all()


def create_book(
        db: Session,
        book: BookCreate
):
    db_book = Book(
        title=book.title,
        summary=book.summary,
        publication_date=book.publication_date,
        author_id=book.publication_date
    )
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book
