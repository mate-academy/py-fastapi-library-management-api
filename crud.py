from sqlalchemy import select
from sqlalchemy.orm import Session

import models
import schemas


def get_all_authors(db: Session, skip: int = 0, limit: int = 10):
    stmt = select(models.Author).offset(skip).limit(limit)
    return db.scalars(stmt).all()

def create_author(db: Session, author: schemas.AuthorCreate):
    new_author = models.Author(
        name=author.name,
        bio=author.bio,
    )
    db.add(new_author)
    db.commit()
    db.refresh(new_author)
    return new_author


def get_author_by_name(db: Session, name: str):
    return (
        db.scalars(select(models.Author).where(models.Author.name == name))
    ).first()


def get_author_by_id(db: Session, author_id: int):
    return db.scalar(
        select(models.Author).where(models.Author.id == author_id))


def get_all_books(db: Session, skip: int = 0, limit: int = 10):
    stmt = select(models.Book).offset(skip).limit(limit)
    return db.scalars(stmt).all()


def get_books_by_author_id(db: Session, author_id: int):
    stmt = select(models.Book).where(models.Book.author_id == author_id)
    return db.scalars(stmt).all()


def create_book_for_author(db: Session, author_id: int,
                           book_data: schemas.BookCreate):
    author = db.get(models.Author, author_id)
    if not author:
        return None

    new_book = models.Book(
        title=book_data.title,
        summary=book_data.summary,
        author_id=author_id
    )
    db.add(new_book)
    db.commit()
    db.refresh(new_book)
    return new_book
