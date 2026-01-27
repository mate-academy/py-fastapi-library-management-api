from sqlalchemy.orm import Session

from models import Author, Book
from schemas import AuthorCreate, BookCreate

def create_author(db: Session, author_in: AuthorCreate) -> Author:
    author = Author(
        name=author_in.name,
        bio=author_in.bio,
    )
    db.add(author)
    db.commit()
    db.refresh(author)
    return author

def get_authors(db: Session, skip: int = 0, limit: int = 100) -> list[Author]:
    return db.query(Author).offset(skip).limit(limit).all()

def get_author_by_id(db: Session, author_id: int) -> Author | None:
    return db.query(Author).filter(Author.id == author_id).first()


def create_book(
        db: Session,
        book_in: BookCreate,
        author_id: int,
) -> Book:
    book = Book(
        title=book_in.title,
        summary=book_in.summary,
        publication_date=book_in.publication_date,
        author_id=author_id
    )
    db.add(book)
    db.commit()
    db.refresh(book)
    return book

def get_books(db: Session, skip: int = 0, limit: int = 100) -> list[Book]:
    return db.query(Book).offset(skip).limit(limit).all()

def get_books_by_author(
    db: Session,
    author_id: int,
    skip: int = 0,
    limit: int = 100,
) -> list[Book]:
    return (
        db.query(Book)
        .filter(Book.author_id == author_id)
        .offset(skip)
        .limit(limit)
        .all()
    )
