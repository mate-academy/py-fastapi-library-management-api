from typing import (
    Optional,
    List,
)
from sqlalchemy.orm import Session
from library_book import models, schemas
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException


def create_author(db: Session, author: schemas.AuthorCreate):
    db_author = models.LBAuthor(name=author.name, bio=author.bio)
    db.add(db_author)
    try:
        db.commit()
        db.refresh(db_author)
        return db_author
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=409, detail="Author with this name already exists.")


def get_authors(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.LBAuthor).offset(skip).limit(limit).all()


def get_author(db: Session, author_id: int):
    return db.query(models.LBAuthor).filter(models.LBAuthor.id == author_id).first()


def create_book(db: Session, author_id: int, book: schemas.BookCreate):
    try:
        db_book = models.LBBook(
            title=book.title,
            summary=book.summary,
            publication_date=book.publication_date,
            packaging_type=book.packaging_type,
            author_id=author_id,
        )
        db.add(db_book)
        db.commit()
        db.refresh(db_book)
        return db_book

    except IntegrityError as e:
        db.rollback()
        if "UNIQUE constraint failed" in str(e.orig):
            raise HTTPException(
                status_code=409,
                detail="Book with this title already exists."
            )
        else:
            raise HTTPException(
                status_code=400,
                detail="Invalid data provided."
            )


def get_books(db: Session, skip: int = 0, limit: int = 10, author_id: Optional[int] = None) -> List[models.LBBook]:
    query = db.query(models.LBBook)

    if author_id is not None:
        query = query.filter(models.LBBook.author_id == author_id)

    return query.offset(skip).limit(limit).all()
