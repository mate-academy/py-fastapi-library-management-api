from sqlalchemy.orm import Session

from db import models
from lib_app import schemas


def get_all_authors(db: Session,
                    skip: int | None = None,
                    limit: int | None = None
                    ):
    return db.query(models.Author).offset(skip).limit(limit).all


def get_author_by_id(db: Session, author_id: int):
    return (db.query(models.Author).
            filter(models.Author.id == author_id).first())


def create_author(db: Session, author: schemas.AuthorCreate) \
        -> "schemas.AuthorCreate":
    db_author = models.Author(
        name=author.name,
        bio=author.bio
    )
    db.add(db_author)
    db.commit()
    db.refresh(db_author)
    return db_author


def get_all_books(db: Session,
                  author: int | None = None,
                  skip: int | None = None,
                  limit: int | None = None
                  ):
    queryset = db.query(models.Book)

    if author is not None:
        queryset = queryset.filter(models.Book.author.has(id=author))

    return queryset.offset(skip).limit(limit).all


def get_book_by_id(db: Session, book_id: int):
    return db.query(models.Book).filter(models.Book.id == book_id).first()


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
