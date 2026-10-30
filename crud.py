from sqlalchemy import select
from sqlalchemy.orm import Session

from models import Author, Book
from schemas import AuthorCreate, BookCreate


def get_all_authors(session: Session, skip: int, limit: int):
    return session.scalars(
        select(Author).offset(skip).limit(limit).order_by(Author.id)
    ).all()


def get_author_by_id(session: Session, author_id: int):
    return session.scalar(select(Author).where(Author.id == author_id))


def create_author(session: Session, author: AuthorCreate):
    db_author = Author(
        name=author.name,
        bio=author.bio,
    )
    session.add(db_author)
    session.commit()
    session.refresh(db_author)

    return db_author


def get_all_books(session: Session, skip: int, limit: int):
    return session.scalars(
        select(Book).offset(skip).limit(limit).order_by(Book.id)
    ).all()


def get_book_by_author_id(session: Session, author_id: int):
    return session.scalars(
        select(Book).where(Book.author_id == author_id)
    ).all()


def create_book(session: Session, book: BookCreate):
    if get_author_by_id(session, book.author_id) is None:
        return None

    db_book = Book(
        title=book.title,
        summary=book.summary,
        publication_date=book.publication_date,
        author_id=book.author_id,
    )
    session.add(db_book)
    session.commit()
    session.refresh(db_book)

    return db_book
