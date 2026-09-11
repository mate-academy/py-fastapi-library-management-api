from sqlalchemy import select
from sqlalchemy.orm import Session

from models import Author, Book
from schemas import AuthorCreate, BookCreate


def get_all_authors(db: Session, skip: int = 0, limit: int = 100):
    return db.scalars(select(Author).offset(skip).limit(limit)).all()


def get_author_by_id(db: Session, author_id: int):
    return db.scalar(select(Author).where(Author.id == author_id))


def get_author_by_name(db: Session, name: str):
    return db.scalar(select(Author).where(Author.name == name))


def create_author(db: Session, author: AuthorCreate):
    author = Author(
        name=author.name,
        bio=author.bio,
    )
    db.add(author)
    db.commit()
    db.refresh(author)

    return author


def get_all_books(
    db: Session, author_id: int | None = None, skip: int = 0, limit: int = 100
):

    stmt = select(Book)
    if author_id:
        stmt = stmt.join(Author).where(Author.id == author_id)
    stmt = stmt.offset(skip).limit(limit)
    return db.scalars(stmt).all()


def create_book(db: Session, book: BookCreate):
    book = Book(
        author_id=book.author_id,
        title=book.title,
        summary=book.summary,
        publication_date=book.publication_date,
    )
    db.add(book)
    db.commit()
    db.refresh(book)
    return book


def get_book_by_id(db: Session, book_id: int):
    return db.scalar(select(Book).where(Book.id == book_id))


def get_book_by_title(db: Session, title: str):
    return db.scalar(select(Book).where(Book.title == title))
