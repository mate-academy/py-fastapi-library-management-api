from sqlalchemy.orm import Session
from typing import Optional
import models
import schemas


# Author CRUD operations
def get_author(db: Session, author_id: int):
    return (
        db.query(models.Author)
        .filter(models.Author.id == author_id)
        .first()
    )


def get_authors(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Author).offset(skip).limit(limit).all()


def create_author(db: Session, author: schemas.AuthorCreate):
    db_author = models.Author(name=author.name, bio=author.bio)
    db.add(db_author)
    db.commit()
    db.refresh(db_author)
    return db_author


def update_author(
    db: Session,
    author_id: int,
    author: schemas.AuthorCreate
):
    db_author = get_author(db, author_id)
    if db_author:
        db_author.name = author.name
        db_author.bio = author.bio
        db.commit()
        db.refresh(db_author)
    return db_author


def delete_author(db: Session, author_id: int):
    db_author = get_author(db, author_id)
    if db_author:
        db.delete(db_author)
        db.commit()
    return db_author


# Book CRUD operations
def get_book(db: Session, book_id: int):
    return db.query(models.Book).filter(models.Book.id == book_id).first()


def get_books(
    db: Session,
    skip: int = 0,
    limit: int = 100,
    author_id: Optional[int] = None
):
    query = db.query(models.Book)
    if author_id:
        query = query.filter(models.Book.author_id == author_id)
    return query.offset(skip).limit(limit).all()


def create_book(db: Session, book: schemas.BookCreate):
    db_book = models.Book(
        title=book.title,
        summary=book.summary,
        publication_date=book.publication_date,
        author_id=book.author_id
    )
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book


def update_book(db: Session, book_id: int, book: schemas.BookCreate):
    db_book = get_book(db, book_id)
    if db_book:
        db_book.title = book.title
        db_book.summary = book.summary
        db_book.publication_date = book.publication_date
        db_book.author_id = book.author_id
        db.commit()
        db.refresh(db_book)
    return db_book


def delete_book(db: Session, book_id: int):
    db_book = get_book(db, book_id)
    if db_book:
        db.delete(db_book)
        db.commit()
    return db_book


def get_books_by_author(
    db: Session,
    author_id: int,
    skip: int = 0,
    limit: int = 100
):
    return (
        db.query(models.Book)
        .filter(models.Book.author_id == author_id)
        .offset(skip)
        .limit(limit)
        .all()
    )
