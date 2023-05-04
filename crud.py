from sqlalchemy.orm import Session

import schemas
from db import models


def create_author(db: Session, author: schemas.AuthorCreate):
    db_author = models.Author(**author.dict())
    db.add(db_author)
    db.commit()
    db.refresh(db_author)

    return db_author


def get_all_authors(db: Session, skip: int = 0, limit: int = 5):
    return db.query(models.Author).offset(skip).limit(limit).all()


def get_author_by_name(db: Session, author_name: str):
    return (
        db.query(models.Author)
        .filter(models.Author.name == author_name)
        .first()
    )


def get_author_by_id(db: Session, author_id: int):
    return (
        db.query(models.Author).filter(models.Author.id == author_id).first()
    )


def delete_author(db: Session, author_id: int):
    db.query(models.Author).filter(models.Author.id == author_id).delete()
    db.commit()
    return {"message": "Author deleted successfully."}


def create_book(db: Session, book: schemas.BookCreate):
    db_book = models.Book(**book.dict())
    db.add(db_book)
    db.commit()
    db.refresh(db_book)

    return db_book


def get_all_books(
    db: Session, author_id: int = None, skip: int = 0, limit: int = 5
):
    query = db.query(models.Book)

    if author_id:
        query = query.filter(models.Book.author_id == author_id)

    return query.offset(skip).limit(limit).all()


def get_book_by_id(db: Session, book_id: int):
    return db.query(models.Book).filter(models.Book.id == book_id).first()


def delete_book(db: Session, book_id: int):
    db.query(models.Book).filter(models.Book.id == book_id).delete()
    db.commit()
    return {"message": "Book deleted successfully."}
