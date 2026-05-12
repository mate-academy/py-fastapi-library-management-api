from sqlalchemy import select
from sqlalchemy.orm import Session

import models
import schemas


def get_authors(db: Session) -> list[models.DBAuthor]:
    return db.scalars(select(models.DBAuthor)).all()


def get_author_by_id(db: Session, author_id: int) -> models.DBAuthor | None:
    return db.scalar(select(models.DBAuthor).where(models.DBAuthor.id == author_id))

def create_author(db: Session, data: schemas.AuthorCreate) -> models.DBAuthor:
    new_author = models.DBAuthor(
        name=data.name,
        bio=data.bio
    )
    db.add(new_author)
    db.commit()
    db.refresh(new_author)
    return new_author


def get_books(db: Session) -> list[models.DBBook]:
    return db.scalars(select(models.DBBook)).all()


def get_book_by_id(db: Session, book_id: int) -> models.DBBook | None:
    return db.scalar(select(models.DBBook).where(models.DBBook.id == book_id))


def create_book(db: Session, data: schemas.BookCreate, author_id: int) -> models.DBBook:
    new_book = models.DBBook(
        title=data.title,
        summary=data.summary,
        publication_date=data.publication_date,
        author_id=author_id
    )
    db.add(new_book)
    db.commit()
    db.refresh(new_book)

    return new_book