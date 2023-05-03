from datetime import date

from sqlalchemy.orm import Session

from models import Author, Book
from schemas import AuthorCreate


def get_authors_list(
        db: Session,
        author_id: int = None,
        limit: int = 10,
        offset: int = 0
):
    query = db.query(Author)
    if author_id:
        query = query.filter(Author.id == author_id)
    query = query.limit(limit).offset(offset)
    return query.all()


def create_author(db: Session, author: AuthorCreate):
    db_author = Author(name=author.name, bio=author.bio)
    db.add(db_author)
    db.commit()
    db.refresh(db_author)
    return db_author


def update_author(
        db: Session,
        author_id: int,
        name: str = None,
        bio: str = None):
    db_author = db.query(Author).filter(Author.id == author_id).first()
    if name:
        db_author.name = name
    if bio:
        db_author.bio = bio
    db.commit()
    db.refresh(db_author)
    return db_author


def get_author_by_name(db: Session, name: int):
    return db.query(Author).filter(Author.name == name).first()


def get_author_by_id(db: Session, author_id: int):
    return db.query(Author).filter(Author.id == author_id).first()


def delete_author(db: Session, author_id: int):
    db_author = db.query(Author).filter(Author.id == author_id).first()
    db.delete(db_author)
    db.commit()
    return db_author


def get_books_list(
        db: Session,
        author_id: int = None,
        limit: int = 10,
        offset: int = 0
):
    query = db.query(Book)
    if author_id:
        return query.filter(Book.author_id == author_id).all()
    query = query.limit(limit).offset(offset)
    return query.all()


def get_book_by_id(db: Session, book_id: int):
    return db.query(Book).filter(Book.id == book_id).first()


def create_book(db: Session, book: Book):
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


def update_book(
        db: Session,
        book_id: int,
        title: str = None,
        summary: str = None,
        publication_date: date = None,
        author_id: int = None,
):
    db_book = db.query(Book).filter(Book.id == book_id).first()
    if title:
        db_book.title = title
    if summary:
        db_book.summary = summary
    if publication_date:
        db_book.publication_date = publication_date
    if author_id:
        db_book.author_id = author_id
    db.commit()
    db.refresh(db_book)
    return db_book


def delete_book(db: Session, book_id: int):
    db_book = db.query(Book).filter(Book.id == book_id).first()
    db.delete(db_book)
    db.commit()
    return db_book
