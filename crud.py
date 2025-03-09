from sqlalchemy.orm import Session
from models import Author, Book
from schemas import AuthorCreate, BookCreate


def create_author(db: Session, author: AuthorCreate) -> Author:
    new_author = Author(**author.model_dump())
    db.add(new_author)
    db.commit()
    db.refresh(new_author)
    return new_author


def get_authors(db: Session, skip: int = 0, limit: int = 10) -> list[Author]:
    return db.query(Author).offset(skip).limit(limit).all()


def get_author(db: Session, author_id: int) -> Author | None:
    return db.query(Author).filter(Author.id == author_id).first()


def create_book(db: Session, book: BookCreate) -> Book:
    new_book = Book(**book.model_dump())
    db.add(new_book)
    db.commit()
    db.refresh(new_book)
    return new_book


def get_books(
        db: Session,
        skip: int = 0,
        limit: int = 10,
        author_id: int | None = None
) -> list[Book]:
    query = db.query(Book)
    if author_id:
        query = query.filter(Book.author_id == author_id)
    return query.offset(skip).limit(limit).all()
