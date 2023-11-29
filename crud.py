from sqlalchemy.orm import Session

import models, schemas


def list_authors(db: Session, skip: int = 0, limit: int = 100) -> list[models.Author]:
    return db.query(models.Author).offset(skip).limit(limit).all()


def get_author(db: Session, author_id: int) -> models.Author:
    return db.query(models.Author).filter(models.Author.id == author_id).first()


def get_author_by_name(db: Session, name: str) -> models.Author:
    return db.query(models.Author).filter(models.Author.name == name).first()


def create_author(db: Session, author: schemas.AuthorCreate) -> models.Author:
    db_author = models.Author(**author.model_dump())
    db.add(db_author)
    db.commit()
    db.refresh(db_author)
    return db_author


def list_books(
    db: Session,
    skip: int = 0,
    limit: int = 100,
    author_id: int | None = None
) -> list[models.Book]:
    queryset = db.query(models.Book)

    if author_id is not None:
        queryset = queryset.filter(
            models.Book.author_id == author_id
        )

    return queryset.offset(skip).limit(limit).all()


def get_book(db: Session, book_id: int) -> models.Book:
    return db.query(models.Book).filter(models.Book.id == book_id).first()


def create_book_for_author(
    db: Session,
    book: schemas.BookCreate,
    author_id: int,
) -> models.Book:
    db_book = models.Book(**book.model_dump(), author_id=author_id)
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book
