from sqlalchemy.orm import Session

import models
import schemas


def _schema_to_dict(schema):
    if hasattr(schema, "model_dump"):
        return schema.model_dump()

    return schema.dict()


def get_author(db: Session, author_id: int) -> models.Author | None:
    return db.query(models.Author).filter(models.Author.id == author_id).first()


def get_author_by_name(db: Session, name: str) -> models.Author | None:
    return db.query(models.Author).filter(models.Author.name == name).first()


def get_authors(db: Session, skip: int = 0, limit: int = 100) -> list[models.Author]:
    return db.query(models.Author).offset(skip).limit(limit).all()


def create_author(db: Session, author: schemas.AuthorCreate) -> models.Author:
    db_author = models.Author(name=author.name, bio=author.bio)
    db.add(db_author)
    db.commit()
    db.refresh(db_author)
    return db_author


def create_book(
    db: Session,
    book: schemas.BookCreate,
    author_id: int,
) -> models.Book:
    db_book = models.Book(**_schema_to_dict(book), author_id=author_id)
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book


def get_books(db: Session, skip: int = 0, limit: int = 100) -> list[models.Book]:
    return db.query(models.Book).offset(skip).limit(limit).all()


def get_books_by_author(
    db: Session,
    author_id: int,
    skip: int = 0,
    limit: int = 100,
) -> list[models.Book]:
    return (
        db.query(models.Book)
        .filter(models.Book.author_id == author_id)
        .offset(skip)
        .limit(limit)
        .all()
    )
