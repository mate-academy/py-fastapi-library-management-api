from sqlalchemy.orm import Session

from db import models
from schemas import AuthorCreate, BookCreate


def get_all_authors(db: Session):
    return db.query(models.DBAuthors).all()


def create_author(db: Session, author: AuthorCreate):
    db_authors = models.DBAuthors(
        name=author.name,
        bio=author.bio
    )
    db.add(db_authors)
    db.commit()
    db.refresh(db_authors)

    return db_authors


def get_all_books(db: Session):
    return db.query(models.DBBook).all()


def get_author_by_id(db: Session, author_id: int):
    return (
        db.query(models.DBAuthors).filter(
            models.DBAuthors.id == author_id
        ).first()
    )


def create_book(db: Session, book: BookCreate):
    db_book = models.DBBook(
        title=book.title,
        summary=book.summary,
        publication_date=book.publication_date
    )
    db.add(db_book)
    db.commit()
    db.refresh(db_book)

    return db_book
