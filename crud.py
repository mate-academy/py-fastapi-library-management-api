from sqlalchemy.orm import Session

import models
from models import Author, Book
from schemas import AuthorSchemaCreate, BookSchemaCreate


def get_author_list(db: Session):
    return db.query(Author).all()


def retrieve_author(db: Session, pk: int):
    return db.query(Author).filter(Author.id == pk).first()


def create_author(db: Session, author: AuthorSchemaCreate) -> Author:
    author = Author(
        name=author.name,
        bio=author.bio
    )
    db.add(author)
    db.commit()
    db.refresh(author)

    return author


def get_book_list(db: Session):
    return db.query(Book).all()


def retrieve_book(db: Session, pk: int):
    return db.query(Book).filter(Book.id == pk).first()


def create_book(db: Session, book: BookSchemaCreate):
    book = Book(
        title=book.title,
        summary=book.summary,
        publication_date=book.publication_date,
        author_id=book.author_id
    )
    db.add(book)
    db.commit()
    db.refresh(book)

    return book
