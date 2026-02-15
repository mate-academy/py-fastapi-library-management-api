from sqlalchemy.orm import Session
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError

import models
import schemas


def get_author(db: Session, author_id: int):
    return db.get(models.Author, author_id)


def get_author_by_name(db: Session, name: str):
    stmt = select(models.Author).where(models.Author.name == name)
    return db.execute(stmt).scalars().first()


def get_authors(db: Session, skip: int = 0, limit: int = 100):
    stmt = select(models.Author).offset(skip).limit(limit)
    return db.execute(stmt).scalars().all()


def create_author(db: Session, author: schemas.AuthorCreate):
    db_author = models.Author(name=author.name, bio=author.bio)
    db.add(db_author)
    try:
        db.commit()
        db.refresh(db_author)
    except IntegrityError:
        db.rollback()
        raise
    return db_author


def create_book_for_author(db: Session, author_id: int, book: schemas.BookCreate):
    db_book = models.Book(
        title=book.title,
        summary=book.summary,
        publication_date=book.publication_date,
        author_id=author_id,
    )
    db.add(db_book)
    try:
        db.commit()
        db.refresh(db_book)
    except IntegrityError:
        db.rollback()
        raise
    return db_book


def get_books(db: Session, skip: int = 0, limit: int = 100, author_id: int | None = None):
    stmt = select(models.Book)
    if author_id is not None:
        stmt = stmt.where(models.Book.author_id == author_id)
    stmt = stmt.offset(skip).limit(limit)
    return db.execute(stmt).scalars().all()
