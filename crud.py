import schemas
from sqlalchemy.orm import Session

from db import models


def get_authors_list(
        db: Session,
        skip: int = 0,
        limit: int = 100,
):
    query = db.query(models.Author)
    query = query.offset(skip).limit(limit)
    return query.all()


def create_author(
        db: Session,
        author: schemas.AuthorCreate,
):
    db_author = models.Author(
        name=author.name,
        bio=author.bio,
    )
    db.add(db_author)
    db.commit()
    db.refresh(db_author)

    return db_author


def get_author_by_id(
        db: Session,
        author_id: int,
):
    return (db.query(models.Author)
            .filter(models.Author.id == author_id).first())


def create_book(
        db: Session,
        book: schemas.BookCreate,
):
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


def get_book_list(
        db: Session,
        skip: int = 0,
        limit: int = 100,
):
    query = db.query(models.Book)
    query = query.offset(skip).limit(limit)
    return query.all()


def filter_book(
        db: Session,
        author_id: int,
):
    return db.query(models.Book).filter(models.Book.author_id == author_id).all()


def get_author_by_name(
        db: Session,
        author_name: str,
):
    return db.query(models.Author).filter(models.Author.name == author_name).first()
