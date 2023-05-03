from fastapi import HTTPException
from sqlalchemy.orm import Session

import models
import schemas


def get_all_authors(db: Session):
    return db.query(models.DBAuthor).all()


def retrieve_author(db: Session, author_id: int):
    author = (
        db.query(models.DBAuthor).
        filter(models.DBAuthor.id == author_id).first()
    )
    if not author:
        raise HTTPException(status_code=404, detail="Author not found")
    return author


def create_author(db: Session, author: schemas.AuthorCreate):
    db_author = models.DBAuthor(
        name=author.name,
        bio=author.bio,
    )
    db.add(db_author)
    db.commit()
    db.refresh(db_author)
    return db_author


def get_all_books(db: Session, author_id: int = None):
    queryset = db.query(models.DBBook)

    if author_id:
        queryset = queryset.filter((models.DBBook.author_id == author_id))

    return queryset.all()


def create_book(db: Session, book: schemas.BookCreate, author_id=None):
    if author_id is None and book.author_id is None:
        raise ValueError("Author ID is required")

    db_book = models.DBBook(
        title=book.title,
        summary=book.summary,
        publication_date=book.publication_date,
        author_id=author_id or book.author_id
    )

    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book


def retrieve_book(db: Session, book_id: int):
    book = db.query(models.DBBook).filter(models.DBBook.id == book_id).first()
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return book
