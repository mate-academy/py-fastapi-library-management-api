from sqlalchemy.orm import Session

from typing import Optional

import schemas
import models
from models import Author, Book


def get_all_authors(skip, limit, db: Session):
    return db.query(Author).offset(skip).limit(limit).all()

def get_author(db: Session, author_id: int):
    return db.query(Author).filter(Author.id == author_id).first()

def create_author(author: schemas.AuthorCreate, db: Session):
    author = models.Author(name=author.name, bio=author.bio)
    db.add(author)
    db.commit()
    db.refresh(author)
    return author

def get_all_books(author_id: Optional[int], skip: int, limit: int, db: Session):
    query = db.query(Book)

    if author_id is not None:
        query = query.filter(Book.author_id == author_id)

    return (
        query.order_by(Book.id)  # ← додаємо сортування
             .offset(skip)
             .limit(limit)
             .all()
    )


def create_book(book: schemas.BookCreate, db: Session):
    book = models.Book(
        title=book.title,
        summary=book.summary,
        publication_date=book.publication_date,
        author_id=book.author_id,
    )
    db.add(book)
    db.commit()
    db.refresh(book)
    return book
