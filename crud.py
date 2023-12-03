from sqlalchemy.orm import Session
import models
import schemas
from typing import Optional


def get_all_authors(db: Session, skip: int = 0, limit: int = 100) -> list[models.Author]:
    return db.query(models.Author).offset(skip).limit(limit).all()


def get_author(db: Session, author_id: int) -> Optional[models.Author]:
    return db.query(models.Author).filter(models.Author.id == author_id).first()


def check_authors_name(db: Session, author_name: str) -> Optional[models.Author]:
    return (
        db.query(models.Author).filter(models.Author.name == author_name).first()
    )


def create_author(db: Session, author: schemas.AuthorCreate) -> models.Author:
    db_author = models.Author(
        name=author.name,
        biography=author.biography,
        books=author.books,
    )

    db.add(db_author)
    db.commit()
    db.refresh(db_author)

    return db_author


def get_all_books(db: Session, skip: int = 0, limit: int = 100) -> list[models.Book]:
    return db.query(models.Book).offset(skip).limit(limit).all()


def filter_book_by_author(
        db: Session,
        author_id: int | None = None
) -> list[models.Book]:
    queryset = db.query(models.Book)

    if author_id:
        queryset = queryset.filter(models.Book.author_id == author_id).first()

    return queryset.all()


def create_book(db: Session, book: schemas.BookCreate) -> models.Book:
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


def create_author_book(db: Session, book: schemas.BookCreate, author_id: int) -> models.Book:
    db_book = models.Book(**book.dict(), author_id=author_id)
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book
