from sqlalchemy.orm import Session

from models import Author, Book
from schemas import AuthorCreate, BookCreate


def get_author_list(db: Session) -> list[Author]:
    return db.query(Author).all()


def get_author(db: Session, author_id: int) -> Author | None:
    return db.query(Author).get(ident=author_id)


def create_author(db: Session, author_create: AuthorCreate) -> Author:
    author = Author(**author_create.model_dump())

    db.add(author)
    db.commit()
    db.refresh(author)
    return author


def get_book_list(db: Session, author_id: int = None) -> list[Book]:
    queryset = db.query(Book)

    if author_id is not None:
        queryset = queryset.filter(Author.id == author_id)

    return queryset.all()


def get_book(db: Session, book_id: int) -> Book | None:
    return db.query(Book).get(ident=book_id)


def create_book(db: Session, book_create: BookCreate) -> Book:
    book = Book(**book_create.model_dump())

    db.add(book)
    db.commit()
    db.refresh(book)
    return book
