from sqlalchemy.orm import Session

import models
import schemas


def get_author_by_id(db: Session, author_id: int):
    return (
        db.query(models.DBAuthor)
        .filter(models.DBAuthor.id == author_id)
        .first()
    )


def get_author_by_name(db: Session, author_name: str):
    return (
        db.query(models.DBAuthor)
        .filter(models.DBAuthor.name == author_name)
        .first()
    )


def get_authors(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.DBAuthor).offset(skip).limit(limit).all()


def create_author(db: Session, author: schemas.AuthorCreate):
    db_author = models.DBAuthor(name=author.name, bio=author.bio)
    db.add(db_author)
    db.commit()
    db.refresh(db_author)
    return db_author


def create_author_book(db: Session, book: schemas.BookCreate, author_id: int):
    db_book = models.DBBook(**book.model_dump(), author_id=author_id)
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book


def get_books(
    db: Session, skip: int = 0, limit: int = 100, author_id: int | None = None
):
    queryset = db.query(models.DBBook)

    if author_id:
        queryset = queryset.filter(models.DBBook.author_id == author_id)

    return queryset.offset(skip).limit(limit).all()
