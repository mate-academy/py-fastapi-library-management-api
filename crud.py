from sqlalchemy import select
from sqlalchemy.orm import Session
import models, schemas


def get_all_authors(db: Session, skip: int = 0, limit: int = 100):
    return db.scalars(select (models.Author)).offset(skip).limit(limit).all()


def get_author_by_id(db: Session, id: int):
    return (
        db.scalar(select(models.Author).where(models.Author.id == id))
    )


def get_author_by_name(db: Session, name: str):
    return (
        db.scalar(select(models.Author).where(models.Author.name == name))
    )


def create_author(db: Session, author: schemas.AuthorCreate):
    db_author = models.Author(
        name=author.name,
        bio=author.bio
    )
    db.add(db_author)
    db.commit()
    db.refresh(db_author)

    return db_author


def create_book(db: Session, book: schemas.BookCreate):
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


def get_all_books(db: Session, skip: int = 0, limit: int = 100):
    return db.scalars(
        select(models.Book)
    ).offset(skip).limit(limit).all()


def get_book_by_title(db: Session, title: str):
    return (
        db.scalar(select(models.Book).where(models.Book.title == title))
    )


def get_book_by_author(
        db: Session,
        author_id: int,
        skip: int = 0,
        limit: int = 100
):
    return db.scalars(
        select(models.Book).where(models.Book.author_id == author_id)
    ).offset(skip).limit(limit).all()
