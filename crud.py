from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session, joinedload

import models
from schemas import BookCreate, BookUpdate, AuthorCreate, AuthorUpdate, AuthorRead


def get_all_books(
        db: Session,
        skip: int = 0,
        limit: int = 10,
        author_id: int | None = None
):
    books = select(models.Book).options(joinedload(models.Book.author)).offset(skip).limit(limit)

    if author_id is not None:
        books = books.where(models.Book.author_id == author_id)

    return db.scalars(books).all()



def create_book(db: Session, book: BookCreate):
    author = db.get(models.Author, book.author_id)
    if not author:
        raise HTTPException(status_code=404, detail="Author not found")

    db_book = models.Book(**book.model_dump())

    db.add(db_book)
    try:
        db.commit()
        db.refresh(db_book)
    except SQLAlchemyError:
        db.rollback()
        raise

    return db_book


def update_book(db: Session, book_id: int, book_data: BookUpdate):
    book = db.get(models.Book, book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")

    for key, value in book_data.model_dump(exclude_unset=True).items():
        setattr(book, key, value)

    db.commit()
    db.refresh(book)
    return book


def get_book(db: Session, book_id: int):
    book = select(
        models.Book
    ).options(joinedload(
        models.Book.author)
    ).where(
        models.Book.id == book_id
    )

    book = db.scalars(book).first()
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return book


def get_all_authors(
        db: Session,
        skip: int = 0,
        limit: int = 10,
):
    authors = select(models.Author).order_by(models.Author.id).offset(skip).limit(limit)
    return db.scalars(authors).all()


def create_author(db: Session, author_data: AuthorCreate):
    db_author = models.Author(**author_data.model_dump())
    db.add(db_author)
    try:
        db.commit()
        db.refresh(db_author)
    except SQLAlchemyError:
        db.rollback()
        raise
    return db_author


def update_author(db: Session, author_id: int, author_data: AuthorUpdate):
    author = db.get(models.Author, author_id)
    if not author:
        raise HTTPException(status_code=404, detail="Author not found")

    for key, value in author_data.model_dump(exclude_unset=True).items():
        setattr(author, key, value)
    db.commit()
    db.refresh(author)
    return author


def get_author(db: Session, author_id: int):
    author = db.get(models.Author, author_id)

    if not author:
        raise HTTPException(status_code=404, detail="Author not found")
    return author

