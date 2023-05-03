from sqlalchemy.orm import Session
from typing import List, Optional

from db import models
import schemas


# Authors CRUD
def get_all_authors(
        db: Session,
        search: Optional[str] = None
) -> List[models.DBAuthor]:
    if search:
        return (db.query(models.DBAuthor)
                .filter(models.DBAuthor.name.icontains(f"%{search}%")).all())
    else:
        return db.query(models.DBAuthor).all()


def get_author(db: Session, author_id: int) -> Optional[models.DBAuthor]:
    return db.query(models.DBAuthor).filter(
        models.DBAuthor.id == author_id
    ).first()


def create_author(
        db: Session,
        author: schemas.AuthorCreate
) -> models.DBAuthor:
    db_author = models.DBAuthor(
        name=author.name,
        bio=author.bio
    )
    db.add(db_author)
    db.commit()
    db.refresh(db_author)
    return db_author


# Books CRUD
def get_all_books(
        db: Session,
        author_id: int | None = None,
        search: Optional[str] = None
) -> List[models.DBBook]:
    query = db.query(models.DBBook)

    if author_id is not None:
        query = query.filter(models.DBBook.author_id == author_id)
    if search:
        return (db.query(models.DBBook)
                .filter(models.DBBook.title.icontains(f"%{search}%")).all())
    else:
        return query.all()


def get_books_by_author(
        db: Session,
        author_id: int,
) -> List[models.DBBook]:
    return db.query(models.DBBook).filter(
        models.DBBook.author_id == author_id
    ).all()


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
