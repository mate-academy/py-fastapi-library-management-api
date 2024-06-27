from sqlalchemy.orm import Session

import models, schemas


# Author CRUD Operations

def get_author(db: Session, author_id: int):
    return db.query(models.Author).filter(
        models.Author.id == author_id
    ).first()


def get_author_by_name(db: Session, name: str):
    return db.query(models.Author).filter(models.Author.name == name).first()


def get_authors(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.Author).offset(skip).limit(limit).all()


def create_author(db: Session, author: schemas.AuthorBase):
    db_author = models.Author(name=author.name, bio=author.bio)
    db.add(db_author)
    db.commit()
    db.refresh(db_author)
    return db_author


def update_author(
    db: Session,
    author_id: int,
    updated_author: schemas.AuthorBase
):
    db_author = get_author(db, author_id)
    if db_author:
        db_author.name = updated_author.name
        db_author.bio = updated_author.bio
        db.commit()
        db.refresh(db_author)
    return db_author


def delete_author(db: Session, author_id: int):
    db_author = get_author(db, author_id)
    if db_author:
        db.delete(db_author)
        db.commit()
    return db_author


# Book CRUD Operations

def get_book(db: Session, book_id: int):
    return db.query(models.Book).filter(models.Book.id == book_id).first()


def get_books(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.Book).offset(skip).limit(limit).all()


def get_books_by_author(
    db: Session,
    author_id: int,
    skip: int = 0,
    limit: int = 10
):
    return db.query(models.Book).filter(
        models.Book.author_id == author_id
    ).offset(skip).limit(limit).all()


def create_book(db: Session, book: schemas.BookBase, author_id: int):
    db_book = models.Book(**book.dict(), author_id=author_id)
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book


def update_book(db: Session, book_id: int, updated_book: schemas.BookBase):
    db_book = get_book(db, book_id)
    if db_book:
        db_book.title = updated_book.title
        db_book.summary = updated_book.summary
        db_book.publication_date = updated_book.publication_date
        db.commit()
        db.refresh(db_book)
    return db_book


def delete_book(db: Session, book_id: int):
    db_book = get_book(db, book_id)
    if db_book:
        db.delete(db_book)
        db.commit()
    return db_book
