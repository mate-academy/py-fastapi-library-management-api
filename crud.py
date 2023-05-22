from sqlalchemy.orm import Session
from db import models
from schemas import AuthorCreate, BookPaginated, BookCreate


def get_all_authors(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.DBAuthor).offset(skip).limit(limit).all()


def get_author_by_id(db: Session, author_id: int):
    return db.query(models.DBAuthor).filter(models.DBAuthor.id == author_id).first()


def create_author(db: Session, author: AuthorCreate):
    db_author = models.DBAuthor(
        name=author.name,
        bio=author.bio,
        books=author.books
    )
    db.add(db_author)
    db.commit()
    db.refresh(db_author)
    return db_author


def create_book_for_author(db: Session, author_id: int, book: BookCreate):
    db_book = models.DBBook(
        title=book.title,
        summary=book.summary,
        publication_date=book.publication_date,
        author_id=author_id
    )
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book


def get_books(db: Session, skip: int = 0, limit: int = 10):
    books = db.query(models.DBBook).offset(skip).limit(limit).all()
    total = db.query(models.DBBook).count()
    return BookPaginated(total=total, skip=skip, limit=limit, items=books)


def filter_books_by_author_id(db: Session, author_id: int, skip: int = 0, limit: int = 10):
    books = db.query(models.DBBook).filter(models.DBBook.author_id == author_id).offset(skip).limit(limit).all()
    total = db.query(models.DBBook).filter(models.DBBook.author_id == author_id).count()
    return BookPaginated(total=total, skip=skip, limit=limit, items=books)
