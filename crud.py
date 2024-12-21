from sqlalchemy.orm import Session

import models
import schemas


def get_all_authors(
        skip: int,
        limit: int,
        db: Session
) -> list[models.DBAuthor]:
    return db.query(models.DBAuthor).offset(skip).limit(limit).all()


def get_author_by_name(db: Session, name: str) -> models.DBAuthor:
    return (
        db.query(
            models.DBAuthor
        ).filter(
            models.DBAuthor.name == name
        ).first()
    )


def get_author_by_id(db: Session, author_id: int) -> models.DBAuthor:
    return (
        db.query(
            models.DBAuthor
        ).filter(
            models.DBAuthor.id == author_id
        ).first()
    )


def create_author(
        db: Session,
        author: schemas.AuthorBaseCreate,
) -> models.DBAuthor:
    db_author = models.DBAuthor(
        name=author.name,
        bio=author.bio
    )
    db.add(db_author)
    db.commit()
    db.refresh(db_author)

    return db_author


def get_books(
        db: Session,
        skip: int,
        limit: int,
        author_id: int | None = None,
) -> list:
    if author_id is not None:
        return (db.query(models.DBBook)
                .filter(models.DBBook.author_id == author_id)
                .offset(skip).limit(limit).all())

    return db.query(models.DBBook).offset(skip).limit(limit).all()


def create_book(db: Session, book: schemas.BookBaseCreate) -> models.DBBook:
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
