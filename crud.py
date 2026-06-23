from sqlalchemy.orm import Session
from sqlalchemy import select
import models
import schemas


def get_author(db: Session, author_id: int):
    return db.scalar(
        select(models.DBAuthor).where(models.DBAuthor.id == author_id)
    )


def get_author_by_name(db: Session, name: str):
    return db.scalar(
        select(models.DBAuthor).where(models.DBAuthor.name == name)
    )


def get_authors(db: Session, skip: int = 0, limit: int = 100):
    result = db.scalars(select(models.DBAuthor).offset(skip).limit(limit))
    return result.all()


def create_author(db: Session, author: schemas.AuthorCreate):
    db_author = models.DBAuthor(name=author.name, bio=author.bio)
    db.add(db_author)
    db.commit()
    db.refresh(db_author)
    return db_author


def get_books(db: Session, skip: int = 0, limit: int = 100):
    result = db.scalars(select(models.DBBook).offset(skip).limit(limit))
    return result.all()


def create_book(db: Session, book: schemas.BookCreate, author_id: int):
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


def get_books_by_author(db: Session, author_id: int):
    result = db.scalars(
        select(models.DBBook).where(models.DBBook.author_id == author_id)
    )
    return result.all()
