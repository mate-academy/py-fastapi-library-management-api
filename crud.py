from sqlalchemy import select
from sqlalchemy.orm import Session

import schemas
from db import models


def get_all_author(db: Session):
    return db.scalars(select(models.DBAuthor)).all()


def get_author_by_name(db: Session, name: str):
    return (
        db.scalars(select(models.DBAuthor).where(models.DBAuthor.name == name)).first()
    )


def create_author(db: Session, author: schemas.AuthorCreate):
    db_author = models.DBAuthor(
        name=author.name,
        bio=author.bio,
    )
    db.add(db_author)
    db.commit()
    db.refresh(db_author)

    return db_author


def get_all_book(db: Session):
    return db.scalars(select(models.DBBook)).all()


def get_book_by_id(db: Session, book_id: int):
    return db.scalars(select(models.DBBook).where(models.DBBook.id == book_id)).first()


def create_book(db: Session, book: schemas.BookCreate, author_id: int):
    db_book = models.DBBook(
        title=book.title,
        summary=book.summary,
        author_id=author_id,
        pub_date=book.pub_date,
    )

    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book
