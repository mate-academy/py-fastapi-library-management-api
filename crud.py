from sqlalchemy import select
from sqlalchemy.orm import Session
import models
import schemas


def get_all_authors(db: Session, skip: int = 0, limit: int = 10):
    return db.scalars(
        select(models.DBAuthor).offset(skip).limit(limit)).all()

def get_author_by_id(db: Session, author_id: int):
    return db.scalars(select(models.DBAuthor).where(
            models.DBAuthor.id == author_id)).one_or_none()

def create_author(db: Session, author: schemas.AuthorCreate):
    db_author = models.DBAuthor(
        name=author.name,
        bio=author.bio
    )
    db.add(db_author)
    db.commit()
    db.refresh(db_author)
    return db_author

def get_all_books(db: Session, skip: int = 0, limit: int = 10):
    return db.scalars(
        select(models.DBBook).offset(skip).limit(limit)).all()

def get_books_by_author_id(db: Session, author_id: int):
    return db.scalars(select(models.DBBook).where(
            models.DBBook.author_id == author_id)).all()

def create_book(
        db: Session,
        book: schemas.BookCreate,
        author_id: int
):
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
