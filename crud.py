from sqlalchemy.orm import Session

from db import models
import schemas


def get_book_by_title(db: Session, title: str) -> schemas.Book:
    return (
        db.query(models.DBBook).filter(models.DBBook.title == title).first()
    )


def get_author_by_name(db: Session, name: str) -> schemas.Author:
    return (
        db.query(models.DBAuthor).filter(models.DBAuthor.name == name).first()
    )


def get_all_book(
        db: Session,
        skip: int = 0,
        limit: int = 100
) -> list[schemas.Book]:
    return db.query(models.DBBook).offset(skip).limit(limit).all()


def create_book(db: Session, book: schemas.BookCreate) -> schemas.Book:
    db_book = models.DBBook(
        title=book.title,
        summary=book.summary,
        publication_date=book.publication_date,
        author_id=book.author_id
    )
    db.add(db_book)
    db.commit()
    db.refresh(db_book)

    return db_book


def get_all_authors(
        db: Session,
        skip: int = 0,
        limit: int = 100
) -> list[schemas.Author]:
    return db.query(models.DBAuthor).offset(skip).limit(limit).all()


def get_author(db: Session, author_id: int) -> schemas.Author:
    return (db.query(models.DBAuthor)
            .filter(models.DBAuthor.id == author_id).first())


def create_author(db: Session, author: schemas.AuthorCreate) -> schemas.Book:
    db_author = models.DBAuthor(
        name=author.name,
        bio=author.bio
    )
    db.add(db_author)
    db.commit()
    db.refresh(db_author)

    return db_author
