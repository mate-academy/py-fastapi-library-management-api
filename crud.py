from fastapi.params import Depends
from sqlalchemy import select
from sqlalchemy.orm import Session
from database import get_db
from models import Book, Author
from schemas import BookCreate, AuthorCreate


def get_books(offset: int, limit: int, db: Session = Depends(get_db)):
    result = db.execute(select(Book).offset(offset).limit(limit))
    books = result.scalars().all()
    return books


def get_book_by_id(id: int, db: Session = Depends(get_db)):
    result = db.execute(select(Book).where(Book.id == id))
    book = result.scalar_one_or_none()
    return book


def create_book(book: BookCreate, db: Session = Depends(get_db)):
    new_book = Book(
        title=book.title,
        summary=book.summary,
        publication_date=book.publication_date,
        author_id=book.author_id,
    )
    db.add(new_book)
    db.commit()
    db.refresh(new_book)
    return new_book


def get_author(offset: int, limit: int, db: Session = Depends(get_db)):
    result = db.execute(select(Author).offset(offset).limit(limit))
    author = result.scalars().all()
    return author


def get_author_by_id(id: int, db: Session = Depends(get_db)):
    result = db.execute(select(Author).where(Author.id == id))
    author = result.scalar_one_or_none()
    return author


def create_author(author: AuthorCreate, db: Session = Depends(get_db)):
    new_author = Author(
        name=author.name,
        bio=author.bio,
    )
    db.add(new_author)
    db.commit()
    db.refresh(new_author)
    return new_author
