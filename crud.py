from sqlalchemy.orm import Session

from models import Author, Book
from schemas import AuthorCreateSchema, BookCreateSchema


def create_author(db: Session, author_in: AuthorCreateSchema) -> Author:
    author = Author(name=author_in.name, bio=author_in.bio)
    db.add(author)
    db.commit()
    db.refresh(author)
    return author


def get_authors(db: Session, skip: int = 0, limit: int = 10) -> list[Author]:
    return db.query(Author).offset(skip).limit(limit).all()


def get_author_by_id(db: Session, author_id: int) -> Author | None:
    return db.query(Author).filter(Author.id == author_id).first()


def create_book_for_author(
    db: Session,
    author_id: int,
    book_in: BookCreateSchema,
) -> Book:
    book = Book(
        title=book_in.title,
        summary=book_in.summary,
        publication_date=book_in.publication_date,
        author_id=author_id,
    )
    db.add(book)
    db.commit()
    db.refresh(book)
    return book


def get_books(
    db: Session,
    skip: int = 0,
    limit: int = 10,
    author_id: int | None = None,
) -> list[Book]:
    q = db.query(Book)
    if author_id is not None:
        q = q.filter(Book.author_id == author_id)
    return q.offset(skip).limit(limit).all()
