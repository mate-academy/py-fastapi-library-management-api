from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from models import Author, Book
from schemas import AuthorCreateSchema, BookCreateSchema


def create_author(db: Session, author_date: AuthorCreateSchema) -> Author:
    author = Author(name=author_date.name, bio=author_date.bio)

    db.add(author)
    db.commit()
    db.refresh(author)
    return author


def author_list(db: Session, skip: int = 0, limit: int = 10) -> list[Author]:
    query = select(Author).offset(skip).limit(limit)
    db_authors = db.execute(query)
    return db_authors.scalars().all()


def get_author_by_id(db: Session, author_id: int) -> Author:
    db_author = db.execute(select(Author).where(Author.id == author_id))
    result = db_author.scalar_one_or_none()

    if not result:
        raise HTTPException(status_code=404, detail="Author not found")

    return result


def create_book(db: Session, book_date: BookCreateSchema) -> Book:
    author = get_author_by_id(db, book_date.author_id)

    book = Book(
        title=book_date.title,
        summary=book_date.summary,
        publication_date=book_date.publication_date,
        author=author,
    )

    db.add(book)
    db.commit()
    db.refresh(book)

    return book


def book_list(
        db: Session,
        skip: int = 0,
        limit: int = 10,
        author_id: int = None
) -> list[Book]:
    query = select(Book)

    if author_id:
        query = query.where(Book.author_id == author_id)

    query = query.offset(skip).limit(limit)
    result = db.execute(query)
    books = result.scalars().all()

    return books
