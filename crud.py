from sqlalchemy import select
from sqlalchemy.orm import Session

import schemas
import models


def get_all_authors(db: Session,
                    skip: int = 0,
                    limit: int = 10,
                    ) -> list[models.DBAutor]:
    return db.query(models.DBAutor).offset(skip).limit(limit).all()

def get_author_by_id(
        db: Session, author_id: int
) -> models.DBAutor | None:
    return db.scalar(
        select(models.DBAutor).where(models.DBAutor.id == author_id) # type: ignore
    )

def create_author(db: Session, author: schemas.AuthorCreate) -> models.DBAutor:
    db_author = models.DBAutor(
        name=author.name,
        bio=author.bio,
    )
    db.add(db_author)
    db.commit()
    db.refresh(db_author)
    return db_author

def get_author_by_name(db: Session, name: str) -> models.DBAutor | None:
    return db.scalar(
        select(models.DBAutor).where(models.DBAutor.name == name) # type: ignore
    )

def get_all_books(
        db: Session,
        skip: int = 0,
        limit: int = 10,
        author_id: int| None = None,
) -> list[models.DBBook] | None:
    stmt = select(models.DBBook) # type: ignore
    if author_id:
        stmt = stmt.where(models.DBBook.author_id == author_id)
    return list(db.scalars(stmt.offset(skip).limit(limit)).all())

def get_book_by_id(db: Session, book_id: int) -> models.DBBook | None:
    return db.scalar(
        select(models.DBBook).where(models.DBBook.id == book_id) # type: ignore
    )

def get_book_by_title(db: Session, title: str) -> models.DBBook | None:
    return db.scalar(
        select(models.DBBook).where(models.DBBook.title == title) # type: ignore
    )

def create_book(db: Session, book: schemas.BookCreate) -> models.DBBook:
    db_book = models.DBBook(
        author_id=book.author_id,
        title=book.title,
        summary=book.summary,
        publication_date=book.publication_date,
    )
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book