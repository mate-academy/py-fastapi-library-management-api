from sqlalchemy.orm import Session

import models
import schemas
from models import DBAuthor


def get_list_of_authors(
        db: Session,
        skip: int | None,
        limit: int | None
) -> list[models.DBAuthor]:

    queryset = db.query(models.DBAuthor)
    if skip:
        queryset = queryset.offset(skip)
    if limit:
        queryset = queryset.limit(limit)
    return queryset.all()


def get_author_by_id(db: Session, author_id: int) -> models.DBAuthor:
    return (
        db.query(models.DBAuthor).filter(models.DBAuthor.id == author_id).first()
    )


def get_author_by_name(db: Session, name: str) -> models.DBAuthor:
    return (
        db.query(models.DBAuthor).filter(
            models.DBAuthor.name == name
        ).first()
    )


def create_author(db: Session, author: schemas.AuthorCreate):
    db_author = DBAuthor(
        name=author.name,
        bio=author.bio
    )
    db.add(db_author)
    db.commit()
    db.refresh(db_author)
    return db_author


def get_book_by_title(db: Session, title: str) -> models.DBBook:
    return (
        db.query(models.DBBook).filter(
            models.DBBook.title == title
        ).first()
    )


def create_book(db: Session, book: schemas.BookCreate) -> models.DBBook:
    db_book = models.DBBook(**book.model_dump())
    db.add(db_book)
    db.commit()
    db.refresh(db_book)

    return db_book


def get_list_of_books(
        db: Session,
        skip: int | None,
        limit: int | None,
        author_id: int | None
) -> list[models.DBBook]:

    queryset = db.query(models.DBBook)
    if skip:
        queryset = queryset.offset(skip)
    if limit:
        queryset = queryset.limit(limit)
    if author_id:
        queryset = queryset.filter(models.DBBook.author_id == author_id)

    return queryset.all()
