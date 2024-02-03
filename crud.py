from sqlalchemy.orm import Session

import models
from models import DBAuthor, DBBook
from schemas import AuthorCreate, Author, BookCreate, Book


def get_all_authors(db: Session):
    return db.query(DBAuthor).all()


def get_author_by_id(db: Session, author_id: int):
    return db.query(DBAuthor).filter(models.DBAuthor.id == author_id).first()


def create_author(db: Session, author: AuthorCreate):
    db_author = models.DBAuthor(name=author.name, bio=author.bio)
    db.add(db_author)
    db.commit()
    db.refresh(db_author)
    return db_author


def update_author(db: Session, author: Author):
    db_author = db.query(DBAuthor).filter(models.DBAuthor.id == author.id).first()
    db_author.name = author.name
    db_author.bio = author.bio
    db.commit()
    db.refresh(db_author)
    return db_author


def delete_author(db: Session, author_id: int):
    db_author = db.query(DBAuthor).filter(models.DBAuthor.id == author_id).first()
    db.delete(db_author)
    db.commit()
    return db_author


def get_all_books(db: Session, author_id: int = None):
    queryset = db.query(DBBook)

    if author_id:
        queryset = queryset.filter(models.DBBook.author_id == author_id)

    return queryset.all()


def get_book_by_title(db: Session, book_title: str):
    return db.query(DBBook).filter(models.DBBook.title == book_title).first()


def create_book(db: Session, book: BookCreate):
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


def update_book(db: Session, book: Book):
    db_book = db.query(DBBook).filter(models.DBBook.id == book.id).first()
    db_book.title = book.title
    db_book.summary = book.summary
    db_book.publication_date = book.publication_date
    db_book.author_id = book.author_id
    db.commit()
    db.refresh(db_book)
    return db_book


def delete_book(db: Session, book_id: int):
    db_book = db.query(DBBook).filter(models.DBBook.id == book_id).first()
    db.delete(db_book)
    db.commit()
    return db_book
