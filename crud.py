from sqlalchemy.orm import Session

import schemas
from db.models import Author, Book


def get_all_authors_with_pagination(db: Session,
                                    skip: int = 0,
                                    limit: int = 10) -> list[Author]:
    authors = db.query(Author).offset(skip).limit(limit).all()
    return authors


def create_author(db: Session, author: schemas.AuthorCreate) -> Author:
    db_author = Author(name=author.name, bio=author.bio)
    db.add(db_author)
    db.commit()
    db.refresh(db_author)
    return db_author


def get_author_by_name(db: Session, name: str) -> Author:
    return db.query(Author).filter(Author.name == name).first()


def get_author_by_id(db: Session, author_id: int) -> Author:
    return db.query(Author).filter(Author.id == author_id).first()


def get_all_books_with_pagination(db: Session,
                                  skip: int = 0,
                                  limit: int = 10,
                                  author_id: int = None) -> list[Book]:
    books = db.query(Book)
    if author_id:
        books = books.filter(Book.author_id == author_id)
    return books.offset(skip).limit(limit).all()


def get_book_by_title(db: Session, title: str) -> Book:
    return db.query(Book).filter(Book.title == title).first()


def create_new_book_with_author(db: Session,
                                book: schemas.BookCreate) -> Book:
    db_book = Book(title=book.title,
                   summary=book.summary,
                   publication_date=book.publication_date,
                   author_id=book.author_id)
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book
