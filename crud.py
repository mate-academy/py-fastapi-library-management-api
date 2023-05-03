from datetime import date

from sqlalchemy.orm import Session

import models
import schemas


def get_authors(
    db: Session,
    skip,
    limit,
):
    return db.query(models.Author).offset(skip).limit(limit).all()


def get_author(db: Session, author_id: int):
    return db.query(models.Author).filter(models.Author.id == author_id).first()


def create_author(db: Session, author: schemas.AuthorCreate):
    db_author = models.Author(name=author.name, bio=author.bio)
    db.add(db_author)
    db.commit()
    db.refresh(db_author)
    return db_author


def update_author(
    db: Session,
    author_id: int,
    name: str = None,
    bio: str = None,
):
    db_author = db.query(models.Author).filter(models.Author.id == author_id)
    author = db_author.first()

    if name:
        author.name = name
    if bio:
        author.bio = bio

    db.commit()
    db.refresh(author)
    return author


def delete_author(db: Session, author_id: int):
    db_author = db.query(models.Author).filter(models.Author.id == author_id)
    author = db_author.first()
    db.delete(author)
    db.commit()
    return author


def get_books(
    db: Session,
    skip,
    limit,
    author_id: int = None,
):
    queryset = db.query(models.Book)
    if author_id is not None:
        queryset = queryset.filter(models.Book.author_id == author_id)
    return queryset.offset(skip).limit(limit).all()


def get_book(db: Session, book_id: int):
    return db.query(models.Book).filter(models.Book.id == book_id).first()


def create_book(db: Session, book: schemas.BookCreate):
    db_book = models.Book(
        title=book.title, summary=book.summary, author_id=book.author_id
    )
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book


def update_book(
    db: Session,
    book_id: int,
    title: str = None,
    summary: str = None,
    author_id: int = None,
    publication_date: date = None,
):
    db_book = db.query(models.Book).filter(models.Book.id == book_id)
    book = db_book.first()

    if title:
        book.title = title
    if summary:
        book.summary = summary
    if author_id:
        book.author_id = author_id
    if publication_date:
        book.publication_date = publication_date

    db.commit()
    db.refresh(book)
    return book


def delete_book(db: Session, book_id: int):
    db_book = db.query(models.Book).filter(models.Book.id == book_id)
    book = db_book.first()
    db.delete(book)
    db.commit()
    return book
