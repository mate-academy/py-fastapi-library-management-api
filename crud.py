from sqlalchemy import select
from sqlalchemy.orm import Session, joinedload

import schemas
from models import Author, Book


def get_author(db: Session, author_id: int):
    result = db.execute(select(Author).options(joinedload(Author.books)).where(Author.id == author_id))
    return result.scalars().unique().one_or_none()


def get_authors(db: Session, skip: int = 0, limit: int = 10):
    return db.execute(select(Author).options(joinedload(Author.books)).offset(skip).limit(limit)).scalars().unique().all()


def create_author(db: Session, author: schemas.AuthorCreate):
    db_author = Author(name=author.name, bio=author.bio)
    db.add(db_author)
    db.commit()
    db.refresh(db_author)

    return db_author


def get_book(db: Session, book_id: int):
    return db.execute(select(Book).options(joinedload(Book.author)).where(Book.id == book_id)).scalar_one_or_none()


def get_books(db: Session, skip: int = 0, limit: int = 10, author_id: int | None = None):
    query = select(Book).where(Book.author_id == author_id)
    return db.execute(query.offset(skip).limit(limit)).scalars().all()


def create_book(db: Session, book: schemas.BookCreate):
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
