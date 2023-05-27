from typing import Optional
from sqlalchemy.orm import Session
import schemas
from db import models


def get_all_author(
        db: Session, skip: int = 0, limit: int = 100
) -> list[models.Author]:
    return db.query(
        models.Author
    ).offset(skip).limit(limit).all()


def get_author(
        db: Session, author_id: int
) -> Optional[models.Author]:
    return db.query(models.Author).filter(
        models.Author.id == author_id
    ).first()


def create_author(
        db: Session, author: schemas.CreateAuthor
) -> models.Author:
    db_author = models.Author(
        name=author.name,
        bio=author.bio,
    )
    db.add(db_author)
    db.commit()
    db.refresh(db_author)
    return db_author


def create_author_book(
        db: Session, book: schemas.CreateBook, author_id: int
) -> models.Book:
    db_book = models.Book(**book.dict(), author_id=author_id)
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book


def get_all_books(
    db: Session,
    skip: int = 0,
    limit: int = 100,
    author_id: str | None = None
) -> list[models.Book]:
    queryset = db.query(models.Book)

    if author_id:
        queryset = queryset.filter(
            models.Book.author_id == int(author_id[0])
        )

    return queryset.offset(skip).limit(limit).all()
