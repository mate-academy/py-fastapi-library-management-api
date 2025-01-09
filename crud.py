from fastapi import HTTPException
from sqlalchemy.orm import Session

import models
import schemas


def get_books(db: Session, author_id: int | None = None, skip: int = 0, limit: int = 100) -> list:
    query = db.query(models.Book)
    if author_id is not None:
        query = query.filter(models.Book.author_id == author_id)
    return query.offset(skip).limit(limit).all()


def create_book(db: Session, book: schemas.BookCreate) -> models.Book:
    book = models.Book(**book.dict())
    db.add(book)
    db.commit()
    db.refresh(book)
    return book


def get_all_author(db: Session, skip: int = 0, limit: int = 100) -> list:
    return db.query(models.Author).offset(skip).limit(limit).all()


def create_author(db: Session, author: schemas.AuthorCreate) -> models.Author:
    author = models.Author(**author.dict())
    db.add(author)
    db.commit()
    db.refresh(author)
    return author


def retrieve_author(db: Session, author_id: int) -> models.Author:
    author = db.query(models.Author).filter(models.Author.id == author_id).first()
    if not author:
        raise HTTPException(status_code=404, detail="Author not found")
    return author

