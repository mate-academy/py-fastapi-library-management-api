from fastapi.exceptions import HTTPException

from database import SessionLocal
from models import DB_Author, DB_Book
from schemas import AuthorCreate, AuthorUpdate, BookCreate, BookUpdate


def read_authors(db: SessionLocal, skip: int | None, limit: int | None):
    if skip and limit:
        return db.query(DB_Author).offset(skip).limit(limit)

    authors = db.query(DB_Author).all()
    return authors


def retrieve_author(db: SessionLocal, author_id: int):
    author = db.query(DB_Author).filter(DB_Author.id == author_id).first()
    if author is None:
        raise HTTPException(status_code=400, detail="Author with given ID not exists")
    return author


def create_author(db: SessionLocal, author_data: AuthorCreate):
    author = DB_Author(
        name=author_data.name,
        bio=author_data.bio
    )
    db.add(author)
    db.commit()
    db.refresh(author)
    return author


def delete_author(db: SessionLocal, author_id: int):
    author = db.query(DB_Author).filter(DB_Author.id == author_id).first()
    if author is None:
        raise HTTPException(status_code=400, detail="Author with given ID not exists")
    db.delete(author)
    db.commit()
    return {"message": "Author was successfully deleted"}


def update_author(db: SessionLocal, author_id: int, author_data: AuthorUpdate):
    author = db.query(DB_Author).filter(DB_Author.id == author_id).first()
    if not author:
        raise HTTPException(status_code=400, detail="Author with given ID not exists")
    if author_data.name:
        author.name = author_data.name
    if author.bio:
        author.bio = author_data.bio
    db.commit()
    db.refresh(author)
    return author


def read_books(db: SessionLocal, skip: int | None, limit: int | None):
    if skip and limit:
        return db.query(DB_Book).offset(skip).limit(limit)

    books = db.query(DB_Book).all()
    return books


def retrieve_book(db: SessionLocal, book_id: int):
    book = db.query(DB_Book).filter(DB_Book.id == book_id).first()
    if book is None:
        raise HTTPException(status_code=400, detail="Book with given ID not exists")
    return book


def create_book(db: SessionLocal, book_data: BookCreate):

    book = DB_Book(
        title=book_data.title,
        summary=book_data.summary,
        publication_date=book_data.publication_date,
        author_id=book_data.author_id
    )
    db.add(book)
    db.commit()
    db.refresh(book)
    return book


def delete_book(db: SessionLocal, book_id: int):
    book = db.query(DB_Book).filter(DB_Book.id == book_id).first()
    if book is None:
        raise HTTPException(status_code=400, detail="Book with given ID not exists")
    db.delete(book)
    db.commit()
    return {"message": "Book was successfully deleted"}


def update_book(db: SessionLocal, book_id: int, book_data: BookUpdate):
    book = db.query(DB_Book).filter(DB_Book.id == book_id).first()
    if not book:
        raise HTTPException(status_code=400, detail="Book with given ID not exists")
    if book_data.title:
        book.title = book_data.title
    if book_data.summary:
        book.data.summary = book_data.summary
    if book_data.publication_date:
        book.publication_date = book_data.publication_date
    if book_data.author_id:
        book.author_id = book_data.author_id
    db.commit()
    db.refresh(book)
    return book
