from sqlalchemy.orm import Session
from db.models import DBAuthor, DBBook
import schemas


def get_author(db: Session, author_id: int):
    return db.query(DBAuthor).filter(DBAuthor.id == author_id).first()


def get_authors(db: Session, skip: int = 0, limit: int = 100):
    return db.query(DBAuthor).offset(skip).limit(limit).all()


def create_author(db: Session, author: schemas.AuthorCreate):
    db_author = DBAuthor(name=author.name, bio=author.bio)
    db.add(db_author)
    db.commit()
    db.refresh(db_author)
    return db_author


def update_author(db: Session, author: schemas.Author):
    db_author = get_author(db, author.id)
    if db_author:
        db_author.name = author.name
        db_author.bio = author.bio
        db.commit()
        db.refresh(db_author)
    return db_author


def delete_author(db: Session, author_id: int):
    db_author = get_author(db, author_id)
    if db_author:
        db.delete(db_author)
        db.commit()
    return db_author


def get_book(db: Session, book_id: int):
    return db.query(DBBook).filter(DBBook.id == book_id).first()


def get_books(db: Session, skip: int = 0, limit: int = 100):
    return db.query(DBBook).offset(skip).limit(limit).all()


def get_books_by_author(db: Session, author_id: int, skip: int = 0, limit: int = 100):
    return db.query(DBBook).filter(DBBook.author_id == author_id).offset(skip).limit(limit).all()


def create_book(db: Session, book: schemas.BookCreate):
    db_book = DBBook(
        title=book.title,
        summary=book.summary,
        publication_date=book.publication_date,
        author_id=book.author_id,
    )
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book


def update_book(db: Session, book: schemas.Book):
    db_book = get_book(db, book.id)
    if db_book:
        db_book.title = book.title
        db_book.summary = book.summary
        db_book.publication_date = book.publication_date
        db_book.author_id = book.author_id
        db.commit()
        db.refresh(db_book)
    return db_book


def delete_book(db: Session, book_id: int):
    db_book = get_book(db, book_id)
    if db_book:
        db.delete(db_book)
        db.commit()
    return db_book
