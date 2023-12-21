from sqlalchemy.orm import Session

import schemas
from db.models import DBAuthor, DBBook
from schemas import AuthorCreate


def create_author(db: Session, author: AuthorCreate) -> DBAuthor:
    db_author = DBAuthor(name=author.name, bio=author.bio)
    db.add(db_author)
    db.commit()
    db.refresh(db_author)

    return db_author


def get_all_authors_with_pagination(
        db: Session,
        skip: int = 0,
        limit: int = 10
) -> list[DBAuthor]:
    authors = db.query(DBAuthor).offset(skip).limit(limit).all()
    return authors


def get_author_by_id(db: Session, author_id: int) -> DBAuthor:
    return db.query(DBAuthor).filter(DBAuthor.id == author_id).first()


def get_author_by_name(db: Session, name: str) -> DBAuthor:
    return db.query(DBAuthor).filter(DBAuthor.name == name).first()


def create_new_book_with_author(db: Session, book: schemas.BookCreate) -> DBBook:
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


def get_book_by_title(db: Session, title: str) -> DBBook:
    return db.query(DBBook).filter(DBBook.title == title).first()


def get_all_books_with_pagination(
        db: Session,
        author_id: int = None,
        skip: int = 0,
        limit: int = 10
) -> list[DBBook]:
    books = db.query(DBBook).offset(skip).limit(limit)

    if author_id is not None:
        books = books.filter(DBBook.author_id == author_id)

    return books.all()
