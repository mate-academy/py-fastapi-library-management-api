from starlette import status
from schemas import CreateAuthor, CreateBook
from models import Author, Book
from sqlalchemy.orm import Session
from fastapi import HTTPException


def create_author(db: Session, author: CreateAuthor):
    add_author = Author(
        name=author.name,
        bio=author.bio
    )
    db.add(add_author)
    db.commit()
    db.refresh(add_author)
    return add_author


def get_authors(db: Session, skip: int = 0, limit: int = 10):
    return db.query(Author).offset(skip).limit(limit).all()


def retrieve_author(db: Session, author_id: int):
    query = db.query(Author).where(Author.id == author_id)
    result = db.execute(query)
    author = result.scalars().first()
    if not author:
        raise HTTPException(
            detail="Author not found",
            status_code=status.HTTP_404_NOT_FOUND
        )
    return author


def create_book(db: Session, book: CreateBook):
    add_book = Book(
        title=book.title,
        summary=book.summary,
        publication_date=book.publication_date,
        author_id=book.author_id
    )
    db.add(add_book)
    db.commit()
    db.refresh(add_book)
    return add_book


def get_books(db: Session, skip: int = 0, limit: int = 10):
    return db.query(Book).offset(skip).limit(limit).all()


def get_books_by_author_id(db: Session, author_id: int):
    query = db.query(Book).where(Book.author_id == author_id)
    result = db.execute(query)
    books = result.scalars().all()
    if not books:
        raise HTTPException(
            detail="Books not found",
            status_code=status.HTTP_404_NOT_FOUND
        )
    return books
