from sqlalchemy.orm import Session

from db import models
from schema import schemas


def get_author_list(db: Session):
    return db.query(models.Author).all()


def get_autor_detail(db: Session, author_id: int):
    return db.query(models.Author).filter(
        models.Author.id == author_id
    ).first()


def create_author(db: Session, author: schemas.AuthorCreate) -> models.Author:
    db_author = models.Author(
        name=author.name,
        bio=author.bio,
    )

    db.add(db_author)
    db.commit()
    db.refresh(db_author)

    return db_author


def get_book_list(author: int | None, db: Session):
    queryset = db.query(models.Book)

    if author is not None:
        queryset = queryset.filter(models.Book.author_id == author)

    return queryset.all()


def get_book_detail(db: Session, book_id: int):
    return db.query(models.Book).filter(models.Book.id == book_id).first()


def create_book(db: Session, book: schemas.BookCreate) -> models.Book:
    db_book = models.Book(
        title=book.title,
        summary=book.summary,
        publication_date=book.publication_date,
        author_id=book.author_id
    )

    db.add(db_book)
    db.commit()
    db.refresh(db_book)

    return db_book
