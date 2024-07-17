from typing import List, Union

from sqlalchemy.orm import Session

from db import models
import schemas


def get_authors_list(db: Session, skip: int = 0, limit: int = 10) -> List[models.AuthorDB]:
    return db.query(models.AuthorDB).offset(skip).limit(limit).all()


def get_author_by_name(db: Session, name: str) -> Union[models.AuthorDB]:
    return (
        db.query(models.AuthorDB).filter(models.AuthorDB.name == name).first()
    )


def get_author(db: Session, author_id: int) -> Union[models.AuthorDB]:
    return db.query(models.AuthorDB).filter(models.AuthorDB.id == author_id).first()


def create_author(db: Session, author: schemas.AuthorCreate) -> models.AuthorDB:
    db_author = models.AuthorDB(
        name=author.name,
        bio=author.bio,
    )
    db.add(db_author)
    db.commit()
    db.refresh(db_author)
    return db_author


def get_book_list(
    db: Session,
    author_id: int | None = None,
    skip: int = 0,
    limit: int = 10,
) -> List[models.BookDB]:
    queryset = db.query(models.BookDB)

    if author_id is not None:
        queryset = queryset.filter(models.BookDB.author_id == author_id)

    return queryset.offset(skip).limit(limit).all()


def create_book(db: Session, book: schemas.BookCreate) -> models.BookDB:
    db_book = models.BookDB(
        title=book.title,
        summary=book.summary,
        publication_date=book.publication_date,
        author_id=book.author_id,
    )
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book
