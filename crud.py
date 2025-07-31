from sqlalchemy.orm import Session

from schemas import AuthorCreateSchema, BookCreateSchema
from db.models import Author, Book


def get_all_authors_with_pagination(
        db: Session,
        skip: int = 0,
        limit: int = 10
):
    return (
        db.query(Author)
        .offset(skip)
        .limit(limit).all()
    )


def get_author_by_id(
        db: Session,
        author_id: int
):
    return (
        db.query(Author)
        .filter(Author.id == author_id)
        .first()
        )


def get_author_by_name(
        db: Session,
        name: str
):
    return (
        db.query(Author)
        .filter(Author.name == name)
        .first()
    )


def create_author(
        db: Session,
        author: AuthorCreateSchema
):
    db_author = Author(
        name=author.name,
        bio=author.bio
    )
    db.add(db_author)
    db.commit()
    db.refresh(db_author)
    return db_author


def get_all_books_with_pagination(
        db: Session,
        skip: int = 0,
        limit: int = 10
):
    return (
        db.query(Book)
        .offset(skip)
        .limit(limit).all()
    )


def get_book_by_id(
        db: Session,
        book_id: int
):
    return (
        db.query(Book)
        .filter(Book.id == book_id)
        .first()
    )


def get_books_by_author_id(
        db: Session,
        author_id: int,
        skip: int = 0,
        limit: int = 10
):
    return (
        db.query(Book)
        .filter(Book.author_id == author_id)
        .offset(skip)
        .limit(limit).all()
    )


def get_book_by_title(
        db: Session,
        title: str
):
    return (
        db.query(Book)
        .filter(Book.title == title)
        .first()
    )


def create_book(
        db: Session,
        book: BookCreateSchema
):
    db_book = Book(
        title=book.title,
        summary=book.summary,
        publication_date=book.publication_date,
        author_id=book.author_id
    )
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book
