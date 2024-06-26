from sqlalchemy.orm import Session
from models import Author, Book
from schemas import AuthorCreate, BookCreate


def get_author_by_name(db: Session, name: str) -> Author:
    return db.query(Author).filter(Author.name == name).first()


def get_all_authors(db: Session, skip: int = 0, limit: int = 10):
    return db.query(Author).offset(skip).limit(limit).all()


def get_author_by_id(db: Session, id: int) -> Author:
    return db.query(Author).filter(Author.id == id).first()


def create_author(db: Session, author: AuthorCreate):
    db_author = Author(
        name=author.name,
        bio=author.bio,
    )
    db.add(db_author)
    db.commit()
    db.refresh(db_author)
    return db_author


def get_all_books(db: Session, skip: int = 0, limit: int = 10):
    return db.query(Book).offset(skip).limit(limit).all()


def get_books_by_author_id(db: Session, author_id: int, skip: int = 0, limit: int = 10):
    return (
        db.query(Book)
        .filter(Book.author_id == author_id)
        .offset(skip)
        .limit(limit)
        .all()
    )


def create_book(db: Session, book: BookCreate):
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
