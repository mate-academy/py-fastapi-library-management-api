from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload

from models import Author, Book
from schemas import AuthorCreate, BookCreate


def get_author_by_id(db: Session, author_id: int) -> Author | None:
    stmt = select(Author).where(Author.id == author_id)
    return db.scalar(stmt)


def get_author_with_books(db: Session, author_id: int) -> Author | None:
    stmt = (
        select(Author)
        .options(selectinload(Author.books))
        .where(Author.id == author_id)
    )
    return db.scalar(stmt)


def get_author_by_name(db: Session, name: str) -> Author | None:
    stmt = select(Author).where(Author.name == name)
    return db.scalar(stmt)


def get_authors(db: Session, skip: int = 0, limit: int = 100) -> list[Author]:
    stmt = select(Author).offset(skip).limit(limit)
    return list(db.scalars(stmt).all())


def create_author(db: Session, author_in: AuthorCreate) -> Author:
    author = Author(name=author_in.name, bio=author_in.bio)
    db.add(author)
    db.commit()
    db.refresh(author)
    return author


def create_book_for_author(db: Session, author_id: int, book_in: BookCreate) -> Book:
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
    limit: int = 100,
    author_id: int | None = None,
) -> list[Book]:
    stmt = select(Book)
    if author_id is not None:
        stmt = stmt.where(Book.author_id == author_id)

    stmt = stmt.offset(skip).limit(limit)
    return list(db.scalars(stmt).all())
