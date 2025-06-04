from sqlalchemy.orm import Session

import schemas
from models import DBAuthor, DBBook
from schemas import AuthorCreate, BookCreate


def get_all_authors(db: Session):
    return db.query(DBAuthor).all()


def get_author_by_id(db: Session, author_id: int):
    return db.query(DBAuthor).filter(DBAuthor.id == author_id).first()


def create_author(db: Session, author: AuthorCreate):
    db_author = DBAuthor(
        name=author.name,
        bio=author.bio
    )
    db.add(db_author)
    db.commit()
    db.refresh(db_author)
    return db_author


def update_author(db: Session, author_id: int, author: schemas.AuthorUpdate):
    db_author = db.query(DBAuthor).filter(DBAuthor.id == author_id).first()
    if db_author:
        db_author.name = author.name
        db_author.bio = author.bio
        db.commit()
        db.refresh(db_author)
    return db_author


def delete_author(db: Session, author_id: int):
    author = db.query(DBAuthor).filter(DBAuthor.id == author_id).first()
    if author:
        db.delete(author)
        db.commit()
    return author


def get_all_books(db: Session):
    return db.query(DBBook).all()


def get_book_by_id(db: Session, book_id: int):
    return db.query(DBBook).filter(DBBook.id == book_id).first()


def create_book(db: Session, book: BookCreate):
    db_book = DBBook(
        title=book.title,
        summary=book.summary,
        publication_date=book.publication_date,
        author_id=book.author_id
    )
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book


def update_book(db: Session, book_id: int, book: schemas.BookUpdate):
    db_book = db.query(DBBook).filter(DBBook.id == book_id).first()
    if db_book:
        db_book.title = book.title
        db_book.summary = book.summary
        db_book.publication_date = book.publication_date
        db_book.author_id = book.author_id
        db.commit()
        db.refresh(db_book)
    return db_book


def delete_book(db: Session, book_id: int):
    book = db.query(DBBook).filter(DBBook.id == book_id).first()
    if book:
        db.delete(book)
        db.commit()
    return book
