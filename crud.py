from sqlalchemy.orm import Session
from typing import Optional, List

import models
import schemas


def create_author(
        db: Session, author: schemas.AuthorCreate
) -> models.DBAuthor:
    author = models.DBAuthor(
        name=author.name,
        bio=author.bio,
    )
    db.add(author)
    db.commit()
    db.refresh(author)

    return author


def authors(db: Session) -> List[models.DBAuthor]:
    return db.query(models.DBAuthor).all()


def author(db: Session, author_id: int) -> models.DBAuthor:
    return db.query(models.DBAuthor).filter(
        models.DBAuthor.id == author_id
    ).first()


def create_book(db: Session, book: schemas.BookCreate) -> models.DBBook:
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


def books(db: Session, author_id: Optional[int] = None) -> List[models.DBBook]:
    queryset = db.query(models.DBBook)

    if author_id:
        queryset = queryset.filter_by(author_id=author_id)

    return queryset
