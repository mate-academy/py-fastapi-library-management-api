from sqlalchemy.orm import Session

import models
import schemas


def get_authors(
        db: Session,
        skip: int = 0,
        limit: int = 10
) -> list[models.DBAuthor]:
    return db.query(models.DBAuthor).offset(skip).limit(limit).all()


def get_author_by_id(
        db: Session,
        author_id: int
) -> models.DBAuthor | None:
    return (
        db.query(models.DBAuthor)
        .filter(models.DBAuthor.id == author_id)
        .first()
    )


def get_author_by_name(
        db: Session,
        name: str
) -> models.DBAuthor | None:
    return (
        db.query(models.DBAuthor)
        .filter(models.DBAuthor.name == name)
        .first()
    )


def create_author(
        db: Session,
        author: schemas.AuthorCreate
) -> models.DBAuthor:
    db_author = models.DBAuthor(
        name=author.name,
        bio=author.bio,
    )
    db.add(db_author)
    db.commit()
    db.refresh(db_author)

    return db_author


def get_books(
        db: Session,
        skip: int = 0,
        limit: int = 10,
        author_id: int | None = None
) -> list[models.DBBook]:
    query = db.query(models.DBBook)

    if author_id is not None:
        query = query.filter(models.DBBook.author_id == author_id)

    return query.offset(skip).limit(limit).all()


def get_book_by_id(
        db: Session,
        book_id: int
) -> models.DBBook | None:
    return db.query(models.DBBook).filter(models.DBBook.id == book_id).first()


def get_book_by_title_and_author(
        db: Session,
        title: str,
        author_id: int
) -> models.DBBook | None:
    return (
        db.query(models.DBBook)
        .filter(
            models.DBBook.title == title,
            models.DBBook.author_id == author_id
        )
        .first()
    )


def create_book(
        db: Session,
        book: schemas.BookCreate
) -> models.DBBook:
    db_book = models.DBBook(
        title=book.title,
        summary=book.summary,
        publication_date=book.publication_date,
        author_id=book.author_id,
    )
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book
