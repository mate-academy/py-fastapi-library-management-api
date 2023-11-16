from fastapi import HTTPException
from sqlalchemy.orm import Session

import schemas
from db import models


def get_authors(db: Session, skip: int = 0, limit: int = 5):
    return db.query(models.Author).offset(skip).limit(limit).all()


def get_books(
    db: Session, skip: int = 0, limit: int = 5, author_id: int = None
):
    query = db.query(models.Book)
    if author_id is not None:
        query = query.filter(models.Book.author_id == author_id)
    return query.offset(skip).limit(limit).all()


def create_author(db: Session, author: schemas.AuthorCreate):
    if (
        db.query(models.Author)
        .filter(models.Author.name == author.name)
        .first()
    ) is None:
        raise HTTPException(status_code=400, detail="This name already exist")

    db_author = models.Author(
        name=author.name,
        bio=author.bio,
    )
    db.add(db_author)
    db.commit()
    db.refresh(db_author)

    return db_author


def get_author_by_id(db: Session, author_id: int):
    db_author = (
        db.query(models.Author).filter(models.Author.id == author_id).first()
    )
    if db_author is None:
        raise HTTPException(status_code=404, detail="Author not found")
    return db_author


def create_book(db: Session, book: schemas.BookCreate):
    if db.query(models.Book).filter(models.Book.title == book.title).first():
        raise HTTPException(status_code=400, detail="This title already exist")

    if (
        db.query(models.Author)
        .filter(models.Author.id == book.author_id)
        .first()
    ) is None:
        raise HTTPException(status_code=400, detail="Author not found")
    db_book = models.Book(
        title=book.title,
        summary=book.summary,
        publication_date=book.publication_date,
        author_id=book.author_id,
    )
    db.add(db_book)
    db.commit()
    db.refresh(db_book)

    return db_book
