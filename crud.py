from sqlalchemy.orm import Session
import models, schemas
from typing import Optional
from sqlalchemy.exc import IntegrityError


def get_author(db: Session, author_id: int) -> Optional[models.DBAuthor]:
    return db.query(models.DBAuthor).filter(models.DBAuthor.id == author_id).first()

def get_authors(
        db: Session,
        skip: int = 0,
        limit: int = 100
) -> list[models.DBAuthor]:
    return db.query(models.DBAuthor).offset(skip).limit(limit).all()

def get_books(
        db: Session,
        skip: int = 0,
        limit: int = 100,
        author_id: Optional[int] = None
) -> list[models.DBBook]:
    query = db.query(models.DBBook)
    if author_id is not None:
       query = query.filter(models.DBBook.author_id == author_id)
    return query.offset(skip).limit(limit).all()

def create_author(db: Session, author: schemas.AuthorCreate):
    db_author = models.DBAuthor(name=author.name, bio=author.bio)

    try:
        db.add(db_author)
        db.commit()
        db.refresh(db_author)
    except IntegrityError:
        db.rollback()
        raise ValueError("Author already exists")

    return db_author


def create_book(db: Session, book: schemas.BookCreate, author_id: int):
    db_author = get_author(db, author_id)
    if db_author is None:
        raise ValueError("Author not found")
    db_book = models.DBBook(
        title=book.title,
        summary=book.summary,
        publication_date=book.publication_date,
        author_id=author_id
    )

    db.add(db_book)

    db.commit()

    db.refresh(db_book)

    return db_book
