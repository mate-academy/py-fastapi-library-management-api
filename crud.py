from sqlalchemy.orm import Session

from models import Book, Author
from schemas import BookCreate


def get_books(db: Session, author_id: int | None) -> list[Book]:
    if author_id:
        return db.query(Book).filter(Book.author_id == author_id).all()

    return db.query(Book).all()


def create_book(db: Session, book: BookCreate):
    db_book = Book(**book.dict())
    db.add(db_book)
    db.commit()
    db.refresh(db_book)

    return db_book


def get_book_by_title(db: Session, title: str):
    return (
        db.query(Book)
        .filter(Book.title == title)
        .first()
    )


def get_authors(db: Session) -> list[Author]:
    return db.query(Author).all()


def get_author_by_id(db: Session, author_id: int) -> Author:
    return db.query(Author).filter_by(id=author_id).first()
