from sqlalchemy.orm import Session

from db.models import Author, Book
from schems import AuthorCreate, BookCreate


def get_all_authors(db: Session) -> list[Author]:
    return db.query(Author).all()


def get_authors_with_pagination(
        db: Session,
        skip: int = 0,
        limit: int = 10
) -> list[Author]:
    return db.query(Author).offset(skip).limit(limit).all()


def get_author_by_name(db: Session, name: str) -> Author | None:
    return db.query(Author).filter(Author.name == name).first()


def get_author_by_id(db: Session, author_id: int) -> Author | None:
    return db.query(Author).filter(Author.id == author_id).first()


def create_author(db: Session, author: AuthorCreate) -> Author:
    db_author = Author(
        name=author.name,
        bio=author.bio
    )
    db.add(db_author)
    db.commit()
    db.refresh(db_author)
    return db_author


def get_all_books(db: Session, author_id: int | None = None) -> list[Book]:
    queryset = db.query(Book)
    if author_id:
        queryset = queryset.filter(Book.author_id == author_id)
    return queryset.all()


def get_books_with_pagination(
        db: Session,
        skip: int = 0,
        limit: int = 10,
        author_id: int | None = None
) -> list[Book]:
    query = db.query(Book)
    if author_id:
        query = query.filter(Book.author_id == author_id)
    return query.offset(skip).limit(limit).all()


def create_book(db: Session, book: BookCreate) -> Book:
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
