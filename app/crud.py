from typing import List

from sqlalchemy.orm import Session
from sqlalchemy.orm.query import Query

from app.db.models import DBAuthor, DBBook
from app.schemas import AuthorCreate, BookCreate


def get_all_authors(db: Session) -> List[DBAuthor]:
    return db.query(DBAuthor).all()


def create_author(db: Session, author: AuthorCreate) -> DBAuthor:
    db_author = DBAuthor(
        name=author.name,
        bio=author.bio
    )
    db.add(db_author)
    db.commit()
    db.refresh(db_author)

    return db_author


def get_author(db: Session, author_id: int) -> DBAuthor:
    return db.query(DBAuthor).get(author_id)


def update_author(
        db: Session,
        author_id: int,
        author_data: AuthorCreate
) -> DBAuthor:
    author = get_author(db=db, author_id=author_id)
    if author is not None:
        author.bio = author_data.bio
        author.name = author_data.name
        db.commit()

        return author


def delete_author(
        db: Session,
        author_id: int
):
    author = get_author(db=db, author_id=author_id)

    if author is not None:
        db.delete(author)
        db.commit()

        return author


def get_all_books(
        db: Session,
        author_id: int | None = None
) -> List[DBBook]:
    queryset = db.query(DBBook)

    if author_id is not None:
        queryset = queryset.filter(DBBook.author_id == author_id)

    return queryset.all()


def create_book(db: Session, book: BookCreate) -> DBBook:
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


def get_book(db: Session, book_id: int) -> DBBook:
    return db.query(DBBook).get(book_id)


def update_book(
        db: Session,
        book_id: int,
        book_data: BookCreate
) -> DBAuthor:
    book = get_book(db=db, book_id=book_id)
    if book is not None:
        book.title = book_data.title
        book.summary = book_data.summary
        book.publication_date = book_data.publication_date
        book.author_id = book_data.author_id
        db.commit()

        return book


def delete_book(db: Session, book_id: int):
    db_book = get_book(db=db, book_id=book_id)
    if db_book is not None:
        db.delete(db_book)
        db.commit()

        return db_book
