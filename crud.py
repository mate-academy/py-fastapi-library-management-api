from typing import List, Optional

from sqlalchemy.orm import Session

import models
import schemas


def get_all_authors(db: Session) -> List[models.Author]:
    return db.query(models.Author).all()


def get_author_by_id(db: Session, author_id: int) -> models.Author:
    return db.query(models.Author).filter(
        models.Author.id == author_id
    ).first()


def create_author(
        db: Session,
        author: schemas.AuthorCreate
) -> models.Author:
    db_author = models.Author(
        name=author.name,
        bio=author.bio,
    )
    db.add(db_author)
    db.commit()
    db.refresh(db_author)

    return db_author


def books(
        db: Session,
        author_id: Optional[int] = None
) -> List[models.Book]:
    queryset = db.query(models.Book)

    if author_id is not None:
        queryset = queryset.filter_by(author_id=author_id)

    return queryset


def create_book(db: Session, book: schemas.BookCreate) -> models.Book:
    db_book = models.Book(
        title=book.title,
        summary=book.summary,
        publication_date=book.publication_date,
        author_id=book.author_id,
    )
    db.add(db_book)
    db.commit()
    db.refresh(db_book)

    return db_book
